"""Run the full recommendation benchmark pipeline."""

from __future__ import annotations

import json
import time

import numpy as np
import pandas as pd

from .als import fit_implicit_als
from .baselines import popularity_score_matrix, popularity_vector
from .batch_score import build_recommendation_table
from .collaborative import fit_bpr_matrix_factorization
from .config import (
    ALS_EPOCHS,
    ALS_FACTORS,
    ALS_REGULARIZATION,
    CANDIDATE_K,
    EPOCHS,
    FACTORS,
    ITEMKNN_NEIGHBORS,
    LEARNING_RATE,
    METRICS_DIR,
    RANKER_WEIGHT_GRID,
    RECOMMENDATIONS_DIR,
    REGULARIZATION,
    REPORTS_DIR,
    SAMPLED_NEGATIVES,
    SEEDS,
    TOP_K,
    ensure_output_dirs,
)
from .content_based import build_user_profiles, score_content_based
from .data_loader import load_movielens_1m
from .evaluation import evaluate_many, evaluate_model, evaluate_sampled_many
from .features import build_genre_matrix, minmax_rows
from .itemknn import fit_itemknn_scores
from .preprocessing import (
    build_user_histories,
    build_user_history_sets,
    build_validation_test_split,
)
from .ranker import (
    apply_candidate_mask,
    build_candidate_mask,
    build_ranker_components,
    combine_components,
)
from .report import build_final_report


def build_long_tail_mask(train: pd.DataFrame, n_items: int, head_fraction: float = 0.20) -> np.ndarray:
    """Mark items outside the top popularity head as long-tail."""
    counts = np.bincount(train["item_idx"].to_numpy(dtype=np.int32), minlength=n_items)
    head_size = max(1, int(round(n_items * head_fraction)))
    head_items = np.argsort(-counts)[:head_size]
    mask = np.ones(n_items, dtype=bool)
    mask[head_items] = False
    return mask


def aggregate_seed_metrics(seed_metrics: pd.DataFrame, top_k: int) -> pd.DataFrame:
    """Aggregate per-seed metrics as mean and std by model."""
    metric_cols = [
        f"precision_at_{top_k}",
        f"recall_at_{top_k}",
        f"map_at_{top_k}",
        f"ndcg_at_{top_k}",
        f"catalog_coverage_at_{top_k}",
        "unique_recommended_items",
        f"avg_distinct_genres_at_{top_k}",
        f"long_tail_share_at_{top_k}",
        f"intra_list_diversity_at_{top_k}",
        f"gini_index_at_{top_k}",
    ]
    rows: list[dict[str, object]] = []
    for model, group in seed_metrics.groupby("model"):
        row: dict[str, object] = {
            "model": model,
            "seeds": int(group["seed"].nunique()),
            "evaluated_users": int(group["evaluated_users"].iloc[0]),
        }
        for col in metric_cols:
            row[f"{col}_mean"] = float(group[col].mean())
            row[f"{col}_std"] = float(group[col].std(ddof=0))
        rows.append(row)
    result = pd.DataFrame(rows)
    return result.sort_values(
        [f"recall_at_{top_k}_mean", f"ndcg_at_{top_k}_mean"],
        ascending=False,
    ).reset_index(drop=True)


def aggregate_sampled_metrics(sampled_metrics: pd.DataFrame, top_k: int) -> pd.DataFrame:
    """Aggregate sampled-negative metrics across seeds."""
    metric_cols = [f"hit_rate_at_{top_k}", f"map_at_{top_k}", f"ndcg_at_{top_k}"]
    rows: list[dict[str, object]] = []
    for model, group in sampled_metrics.groupby("model"):
        row: dict[str, object] = {
            "model": model,
            "seeds": int(group["seed"].nunique()),
            "evaluated_users": int(group["evaluated_users"].iloc[0]),
            "sampled_negatives": int(group["sampled_negatives"].iloc[0]),
        }
        for col in metric_cols:
            row[f"{col}_mean"] = float(group[col].mean())
            row[f"{col}_std"] = float(group[col].std(ddof=0))
        rows.append(row)
    return pd.DataFrame(rows).sort_values(f"hit_rate_at_{top_k}_mean", ascending=False)


def tune_ranker(
    components: dict[str, np.ndarray],
    candidate_mask: np.ndarray,
    histories: list[np.ndarray],
    validation: pd.DataFrame,
    item_features: np.ndarray,
    long_tail_mask: np.ndarray,
    seed: int,
) -> tuple[dict[str, float], pd.DataFrame]:
    """Tune ranker weights on validation holdout."""
    rows: list[dict[str, object]] = []
    for weights in RANKER_WEIGHT_GRID:
        combined = combine_components(components, weights)
        reranked = apply_candidate_mask(combined, candidate_mask)
        metrics = evaluate_model(
            model_name=str(weights["name"]),
            scores=reranked,
            histories=histories,
            test=validation,
            item_features=item_features,
            long_tail_mask=long_tail_mask,
            k=TOP_K,
        )
        metrics["seed"] = seed
        for key, value in weights.items():
            metrics[f"weight_{key}"] = value
        rows.append(metrics)

    validation_metrics = pd.DataFrame(rows).sort_values(
        [f"recall_at_{TOP_K}", f"ndcg_at_{TOP_K}", f"catalog_coverage_at_{TOP_K}"],
        ascending=False,
    )
    best_name = str(validation_metrics.iloc[0]["weight_name"])
    best_weights = next(weights for weights in RANKER_WEIGHT_GRID if weights["name"] == best_name)
    return best_weights, validation_metrics


def run_cold_start_experiment(
    train: pd.DataFrame,
    test: pd.DataFrame,
    items: pd.DataFrame,
    n_users: int,
    n_items: int,
    item_features: np.ndarray,
    long_tail_mask: np.ndarray,
) -> pd.DataFrame:
    """Simulate low-interaction items being hidden from collaborative training."""
    counts = np.bincount(train["item_idx"].to_numpy(dtype=np.int32), minlength=n_items)
    nonzero_counts = counts[counts > 0]
    cutoff = int(np.quantile(nonzero_counts, 0.25))
    cold_items = np.where((counts > 0) & (counts <= max(cutoff, 1)))[0]
    cold_test = test[test["item_idx"].isin(cold_items)].copy()

    if cold_test.empty:
        return pd.DataFrame(
            [
                {
                    "model": "no_cold_items_available",
                    "cold_items": int(len(cold_items)),
                    "evaluated_users": 0,
                }
            ]
        )

    cold_train = train[~train["item_idx"].isin(cold_items)].copy()
    histories = build_user_histories(cold_train, n_users)

    popularity = popularity_vector(cold_train, n_items)
    popularity_scores = popularity_score_matrix(popularity, n_users)

    user_profiles = build_user_profiles(histories, item_features)
    content_scores = score_content_based(user_profiles, item_features)

    novelty = 1.0 - popularity_scores
    hybrid_fallback = (
        0.65 * minmax_rows(content_scores)
        + 0.10 * popularity_scores
        + 0.25 * novelty
    ).astype(np.float32)

    matrices = {
        "cold_popularity_fallback": popularity_scores,
        "cold_content_fallback": content_scores,
        "cold_hybrid_fallback": hybrid_fallback,
    }
    result = evaluate_many(matrices, histories, cold_test, item_features, long_tail_mask, TOP_K)
    result["cold_items_hidden_from_collaborative_training"] = int(len(cold_items))
    result["cold_item_popularity_cutoff"] = int(max(cutoff, 1))
    return result


def main() -> None:
    start_time = time.perf_counter()
    ensure_output_dirs()

    ratings, items = load_movielens_1m()
    n_users = int(ratings["user_idx"].nunique())
    n_items = int(items["item_idx"].nunique())

    train, validation, test = build_validation_test_split(ratings)
    histories = build_user_histories(train, n_users)
    history_sets = build_user_history_sets(histories)
    item_features, genres = build_genre_matrix(items)
    long_tail_mask = build_long_tail_mask(train, n_items)

    print("Building deterministic baselines")
    popularity = popularity_vector(train, n_items)
    popularity_scores = popularity_score_matrix(popularity, n_users)
    user_profiles = build_user_profiles(histories, item_features)
    content_scores = score_content_based(user_profiles, item_features)
    itemknn_scores = fit_itemknn_scores(train, n_users, n_items, ITEMKNN_NEIGHBORS)

    seed_metric_frames: list[pd.DataFrame] = []
    sampled_metric_frames: list[pd.DataFrame] = []
    validation_frames: list[pd.DataFrame] = []
    best_ranker_rows: list[dict[str, object]] = []
    best_scores_by_seed: dict[int, np.ndarray] = {}

    for seed in SEEDS:
        print(f"Running seed {seed}")
        bpr_model = fit_bpr_matrix_factorization(
            train=train,
            history_sets=history_sets,
            n_users=n_users,
            n_items=n_items,
            factors=FACTORS,
            epochs=EPOCHS,
            learning_rate=LEARNING_RATE,
            regularization=REGULARIZATION,
            seed=seed,
        )
        bpr_scores = bpr_model.score_all()

        als_model = fit_implicit_als(
            train=train,
            n_users=n_users,
            n_items=n_items,
            factors=ALS_FACTORS,
            epochs=ALS_EPOCHS,
            regularization=ALS_REGULARIZATION,
            seed=seed,
        )
        als_scores = als_model.score_all()

        candidate_mask = build_candidate_mask(
            [bpr_scores, als_scores, itemknn_scores],
            histories,
            CANDIDATE_K,
        )
        components = build_ranker_components(
            bpr_scores=bpr_scores,
            als_scores=als_scores,
            itemknn_scores=itemknn_scores,
            content_scores=content_scores,
            popularity_scores=popularity_scores,
        )
        best_weights, validation_metrics = tune_ranker(
            components,
            candidate_mask,
            histories,
            validation,
            item_features,
            long_tail_mask,
            seed,
        )
        validation_frames.append(validation_metrics)
        best_ranker_rows.append({"seed": seed, **best_weights})

        score_blend = combine_components(components, best_weights)
        two_stage_ranker = apply_candidate_mask(score_blend, candidate_mask)
        best_scores_by_seed[seed] = two_stage_ranker

        score_matrices = {
            "popularity": popularity_scores,
            "content_based": content_scores,
            "itemknn": itemknn_scores,
            "bpr_matrix_factorization": bpr_scores,
            "implicit_als": als_scores,
            "hybrid_score_blend": score_blend,
            "two_stage_hybrid_ranker": two_stage_ranker,
        }

        seed_metrics = evaluate_many(
            score_matrices,
            histories,
            test,
            item_features,
            long_tail_mask,
            TOP_K,
        )
        seed_metrics["seed"] = seed
        seed_metric_frames.append(seed_metrics)

        sampled_metrics = evaluate_sampled_many(
            score_matrices,
            histories,
            test,
            TOP_K,
            SAMPLED_NEGATIVES,
            seed,
        )
        sampled_metrics["seed"] = seed
        sampled_metric_frames.append(sampled_metrics)

    seed_metrics = pd.concat(seed_metric_frames, ignore_index=True)
    seed_metrics.to_csv(METRICS_DIR / "seed_metrics.csv", index=False)

    model_comparison = aggregate_seed_metrics(seed_metrics, TOP_K)
    model_comparison.to_csv(METRICS_DIR / "model_comparison.csv", index=False)

    validation_metrics = pd.concat(validation_frames, ignore_index=True)
    validation_metrics.to_csv(METRICS_DIR / "hyperparameter_search.csv", index=False)
    pd.DataFrame(best_ranker_rows).to_csv(METRICS_DIR / "selected_ranker_weights.csv", index=False)

    sampled_metrics = pd.concat(sampled_metric_frames, ignore_index=True)
    sampled_metrics.to_csv(METRICS_DIR / "sampled_100_negative_seed_metrics.csv", index=False)
    sampled_summary = aggregate_sampled_metrics(sampled_metrics, TOP_K)
    sampled_summary.to_csv(METRICS_DIR / "sampled_100_negative_metrics.csv", index=False)

    cold_start = run_cold_start_experiment(
        train,
        test,
        items,
        n_users,
        n_items,
        item_features,
        long_tail_mask,
    )
    cold_start.to_csv(METRICS_DIR / "cold_start_experiment.csv", index=False)

    coverage_columns = [
        "model",
        f"catalog_coverage_at_{TOP_K}_mean",
        f"catalog_coverage_at_{TOP_K}_std",
        "unique_recommended_items_mean",
        f"long_tail_share_at_{TOP_K}_mean",
        f"gini_index_at_{TOP_K}_mean",
    ]
    model_comparison[coverage_columns].to_csv(METRICS_DIR / "catalog_coverage.csv", index=False)

    best_model = str(model_comparison.iloc[0]["model"])
    best_seed_row = seed_metrics[seed_metrics["model"] == best_model].sort_values(
        [f"recall_at_{TOP_K}", f"ndcg_at_{TOP_K}"],
        ascending=False,
    ).iloc[0]
    best_seed = int(best_seed_row["seed"])
    recommendation_scores = best_scores_by_seed.get(best_seed)
    if recommendation_scores is None:
        recommendation_scores = best_scores_by_seed[SEEDS[0]]

    user_lookup = ratings[["user_idx", "user_id"]].drop_duplicates().sort_values("user_idx")
    recommendations = build_recommendation_table(
        model_name=best_model,
        scores=recommendation_scores,
        histories=histories,
        items=items,
        user_lookup=user_lookup,
        sample_user_count=25,
        k=TOP_K,
    )
    recommendations.to_csv(RECOMMENDATIONS_DIR / "sample_user_recommendations.csv", index=False)

    positive_count = int((ratings["rating"] >= 4).sum())
    rated_item_count = int(ratings["item_idx"].nunique())
    sparsity_percent = 100.0 * (1.0 - len(ratings) / (n_users * n_items))
    dataset_summary = {
        "ratings": int(len(ratings)),
        "users": n_users,
        "items": n_items,
        "rated_items": rated_item_count,
        "positive_interactions": positive_count,
        "train_positive_interactions": int(len(train)),
        "validation_users": int(len(validation)),
        "evaluation_users": int(len(test)),
        "sparsity_percent": sparsity_percent,
        "genres": len(genres),
        "seeds": SEEDS,
        "candidate_k": CANDIDATE_K,
        "sampled_negatives": SAMPLED_NEGATIVES,
        "runtime_seconds": round(time.perf_counter() - start_time, 2),
    }
    with (METRICS_DIR / "dataset_summary.json").open("w", encoding="utf-8") as file:
        json.dump(dataset_summary, file, indent=2)

    report = build_final_report(
        model_comparison,
        dataset_summary,
        best_model,
        TOP_K,
        sampled_summary,
        cold_start,
    )
    (REPORTS_DIR / "final_report.md").write_text(report, encoding="utf-8")

    print("Pipeline complete")
    print(f"Best model: {best_model}")
    print(model_comparison.to_string(index=False))


if __name__ == "__main__":
    main()
