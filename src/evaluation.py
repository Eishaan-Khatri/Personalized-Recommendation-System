"""Ranking evaluation helpers."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def top_k_for_user(scores: np.ndarray, k: int) -> np.ndarray:
    """Return item indices sorted by descending score."""
    candidate_count = min(k, len(scores))
    top = np.argpartition(-scores, candidate_count - 1)[:candidate_count]
    return top[np.argsort(-scores[top])]


def gini_index(counts: np.ndarray) -> float:
    """Compute Gini concentration over recommendation counts."""
    values = np.sort(counts.astype(np.float64))
    total = values.sum()
    if total <= 0:
        return 0.0
    n = len(values)
    index = np.arange(1, n + 1)
    return float(((2 * index - n - 1) * values).sum() / (n * total))


def _intra_list_diversity(top_items: np.ndarray, normalized_item_features: np.ndarray) -> float:
    """Mean pairwise genre dissimilarity inside a recommendation list."""
    if len(top_items) <= 1:
        return 0.0
    vectors = normalized_item_features[top_items]
    similarity = vectors @ vectors.T
    upper = similarity[np.triu_indices(len(top_items), k=1)]
    return float(1.0 - np.mean(upper))


def evaluate_model(
    model_name: str,
    scores: np.ndarray,
    histories: list[np.ndarray],
    test: pd.DataFrame,
    item_features: np.ndarray,
    long_tail_mask: np.ndarray,
    k: int,
) -> dict[str, float | int | str]:
    """Evaluate a score matrix with one held-out item per user."""
    hits = 0
    average_precision = 0.0
    ndcg = 0.0
    recommended_items: list[int] = []
    distinct_genres_per_user: list[int] = []
    long_tail_hits = 0
    total_recommendations = 0
    recommendation_counts = np.zeros(scores.shape[1], dtype=np.int32)
    normalized_item_features = item_features / np.maximum(
        np.linalg.norm(item_features, axis=1, keepdims=True),
        1e-8,
    )
    intra_list_diversities: list[float] = []

    test_users = test["user_idx"].to_numpy(dtype=np.int32)
    test_items = test["item_idx"].to_numpy(dtype=np.int32)

    for user_idx, heldout_item in zip(test_users, test_items, strict=True):
        user_scores = scores[user_idx].copy()
        seen = histories[int(user_idx)]
        if len(seen) > 0:
            user_scores[seen] = -np.inf

        top_items = top_k_for_user(user_scores, k)
        recommended_items.extend(map(int, top_items))
        recommendation_counts[top_items] += 1
        long_tail_hits += int(long_tail_mask[top_items].sum())
        total_recommendations += len(top_items)
        if len(top_items) > 0:
            genre_count = int((item_features[top_items].sum(axis=0) > 0).sum())
            distinct_genres_per_user.append(genre_count)
            intra_list_diversities.append(_intra_list_diversity(top_items, normalized_item_features))

        matches = np.where(top_items == int(heldout_item))[0]
        if len(matches) > 0:
            rank = int(matches[0]) + 1
            hits += 1
            average_precision += 1.0 / rank
            ndcg += 1.0 / math.log2(rank + 1)

    evaluated_users = len(test_users)
    unique_recommended = len(set(recommended_items))
    n_items = scores.shape[1]
    return {
        "model": model_name,
        "evaluated_users": evaluated_users,
        f"precision_at_{k}": hits / (evaluated_users * k),
        f"recall_at_{k}": hits / evaluated_users,
        f"map_at_{k}": average_precision / evaluated_users,
        f"ndcg_at_{k}": ndcg / evaluated_users,
        f"catalog_coverage_at_{k}": unique_recommended / n_items,
        "unique_recommended_items": unique_recommended,
        f"avg_distinct_genres_at_{k}": float(np.mean(distinct_genres_per_user)),
        f"long_tail_share_at_{k}": long_tail_hits / max(total_recommendations, 1),
        f"intra_list_diversity_at_{k}": float(np.mean(intra_list_diversities)),
        f"gini_index_at_{k}": gini_index(recommendation_counts),
    }


def evaluate_many(
    score_matrices: dict[str, np.ndarray],
    histories: list[np.ndarray],
    test: pd.DataFrame,
    item_features: np.ndarray,
    long_tail_mask: np.ndarray,
    k: int,
) -> pd.DataFrame:
    """Evaluate multiple models into one table."""
    rows = [
        evaluate_model(name, scores, histories, test, item_features, long_tail_mask, k)
        for name, scores in score_matrices.items()
    ]
    return pd.DataFrame(rows)


def evaluate_sampled_negatives(
    model_name: str,
    scores: np.ndarray,
    histories: list[np.ndarray],
    test: pd.DataFrame,
    k: int,
    negatives: int,
    seed: int,
) -> dict[str, float | int | str]:
    """Evaluate with one positive item and sampled negatives per user."""
    rng = np.random.default_rng(seed)
    n_items = scores.shape[1]
    hits = 0
    average_precision = 0.0
    ndcg = 0.0

    for row in test.itertuples(index=False):
        user_idx = int(row.user_idx)
        heldout = int(row.item_idx)
        blocked = set(map(int, histories[user_idx]))
        blocked.add(heldout)

        sampled: list[int] = []
        while len(sampled) < negatives:
            item_idx = int(rng.integers(n_items))
            if item_idx not in blocked:
                sampled.append(item_idx)
                blocked.add(item_idx)

        candidates = np.array([heldout, *sampled], dtype=np.int32)
        candidate_scores = scores[user_idx, candidates]
        top_local = top_k_for_user(candidate_scores, min(k, len(candidates)))
        ranked_items = candidates[top_local]
        matches = np.where(ranked_items == heldout)[0]
        if len(matches) > 0:
            rank = int(matches[0]) + 1
            hits += 1
            average_precision += 1.0 / rank
            ndcg += 1.0 / math.log2(rank + 1)

    evaluated_users = len(test)
    return {
        "model": model_name,
        "evaluated_users": evaluated_users,
        "sampled_negatives": negatives,
        f"hit_rate_at_{k}": hits / evaluated_users,
        f"map_at_{k}": average_precision / evaluated_users,
        f"ndcg_at_{k}": ndcg / evaluated_users,
    }


def evaluate_sampled_many(
    score_matrices: dict[str, np.ndarray],
    histories: list[np.ndarray],
    test: pd.DataFrame,
    k: int,
    negatives: int,
    seed: int,
) -> pd.DataFrame:
    """Sampled-negative evaluation for multiple models."""
    rows = [
        evaluate_sampled_negatives(name, scores, histories, test, k, negatives, seed)
        for name, scores in score_matrices.items()
    ]
    return pd.DataFrame(rows)
