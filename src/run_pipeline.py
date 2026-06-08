"""Run the end-to-end recommendation pipeline."""

from __future__ import annotations

import json
import time

import pandas as pd

from .baselines import popularity_score_matrix, popularity_vector
from .batch_score import build_recommendation_table
from .collaborative import fit_bpr_matrix_factorization
from .config import (
    EPOCHS,
    FACTORS,
    HYBRID_WEIGHTS,
    LEARNING_RATE,
    METRICS_DIR,
    RECOMMENDATIONS_DIR,
    REGULARIZATION,
    REPORTS_DIR,
    RANDOM_SEED,
    TOP_K,
    ensure_output_dirs,
)
from .content_based import build_user_profiles, score_content_based
from .data_loader import load_movielens_1m
from .evaluation import evaluate_many
from .features import build_genre_matrix
from .hybrid import build_hybrid_scores
from .preprocessing import build_holdout_split, build_user_histories, build_user_history_sets
from .report import build_final_report


def main() -> None:
    start_time = time.perf_counter()
    ensure_output_dirs()

    ratings, items = load_movielens_1m()
    n_users = int(ratings["user_idx"].nunique())
    n_items = int(items["item_idx"].nunique())

    train, test = build_holdout_split(ratings)
    histories = build_user_histories(train, n_users)
    history_sets = build_user_history_sets(histories)
    item_features, genres = build_genre_matrix(items)

    popularity = popularity_vector(train, n_items)
    popularity_scores = popularity_score_matrix(popularity, n_users)

    user_profiles = build_user_profiles(histories, item_features)
    content_scores = score_content_based(user_profiles, item_features)

    mf_model = fit_bpr_matrix_factorization(
        train=train,
        history_sets=history_sets,
        n_users=n_users,
        n_items=n_items,
        factors=FACTORS,
        epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        regularization=REGULARIZATION,
        seed=RANDOM_SEED,
    )
    collaborative_scores = mf_model.score_all()
    hybrid_scores = build_hybrid_scores(
        collaborative_scores=collaborative_scores,
        content_scores=content_scores,
        popularity_scores=popularity_scores,
        weights=HYBRID_WEIGHTS,
    )

    score_matrices = {
        "popularity": popularity_scores,
        "content_based": content_scores,
        "collaborative_filtering": collaborative_scores,
        "hybrid": hybrid_scores,
    }
    metrics = evaluate_many(score_matrices, histories, test, item_features, TOP_K)
    metrics = metrics.sort_values([f"recall_at_{TOP_K}", f"ndcg_at_{TOP_K}"], ascending=False)
    metrics.to_csv(METRICS_DIR / "model_comparison.csv", index=False)

    coverage = metrics[["model", f"catalog_coverage_at_{TOP_K}", "unique_recommended_items"]].copy()
    coverage.to_csv(METRICS_DIR / "catalog_coverage.csv", index=False)

    user_lookup = ratings[["user_idx", "user_id"]].drop_duplicates().sort_values("user_idx")
    best_model = str(metrics.iloc[0]["model"])
    recommendation_scores = score_matrices[best_model]
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
    sparsity_percent = 100.0 * (1.0 - len(ratings) / (n_users * n_items))
    dataset_summary = {
        "ratings": int(len(ratings)),
        "users": n_users,
        "items": n_items,
        "positive_interactions": positive_count,
        "train_positive_interactions": int(len(train)),
        "evaluation_users": int(len(test)),
        "sparsity_percent": sparsity_percent,
        "genres": len(genres),
        "runtime_seconds": round(time.perf_counter() - start_time, 2),
    }
    with (METRICS_DIR / "dataset_summary.json").open("w", encoding="utf-8") as file:
        json.dump(dataset_summary, file, indent=2)

    report = build_final_report(metrics, dataset_summary, best_model, TOP_K)
    (REPORTS_DIR / "final_report.md").write_text(report, encoding="utf-8")

    print("Pipeline complete")
    print(f"Best model: {best_model}")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
