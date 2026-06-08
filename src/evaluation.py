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


def evaluate_model(
    model_name: str,
    scores: np.ndarray,
    histories: list[np.ndarray],
    test: pd.DataFrame,
    item_features: np.ndarray,
    k: int,
) -> dict[str, float | int | str]:
    """Evaluate a score matrix with one held-out item per user."""
    hits = 0
    average_precision = 0.0
    ndcg = 0.0
    recommended_items: list[int] = []
    distinct_genres_per_user: list[int] = []

    test_users = test["user_idx"].to_numpy(dtype=np.int32)
    test_items = test["item_idx"].to_numpy(dtype=np.int32)

    for user_idx, heldout_item in zip(test_users, test_items, strict=True):
        user_scores = scores[user_idx].copy()
        seen = histories[int(user_idx)]
        if len(seen) > 0:
            user_scores[seen] = -np.inf

        top_items = top_k_for_user(user_scores, k)
        recommended_items.extend(map(int, top_items))
        if len(top_items) > 0:
            genre_count = int((item_features[top_items].sum(axis=0) > 0).sum())
            distinct_genres_per_user.append(genre_count)

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
    }


def evaluate_many(
    score_matrices: dict[str, np.ndarray],
    histories: list[np.ndarray],
    test: pd.DataFrame,
    item_features: np.ndarray,
    k: int,
) -> pd.DataFrame:
    """Evaluate multiple models into one table."""
    rows = [
        evaluate_model(name, scores, histories, test, item_features, k)
        for name, scores in score_matrices.items()
    ]
    return pd.DataFrame(rows)
