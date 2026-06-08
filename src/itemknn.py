"""Collaborative ItemKNN recommender."""

from __future__ import annotations

import numpy as np
import pandas as pd


def build_user_item_matrix(train: pd.DataFrame, n_users: int, n_items: int) -> np.ndarray:
    """Build a dense binary user-item interaction matrix."""
    matrix = np.zeros((n_users, n_items), dtype=np.float32)
    users = train["user_idx"].to_numpy(dtype=np.int32)
    items = train["item_idx"].to_numpy(dtype=np.int32)
    matrix[users, items] = 1.0
    return matrix


def fit_itemknn_scores(
    train: pd.DataFrame,
    n_users: int,
    n_items: int,
    neighbors: int,
) -> np.ndarray:
    """Score items by cosine similarity to each user's interacted items."""
    user_item = build_user_item_matrix(train, n_users, n_items)
    item_user = user_item.T
    norms = np.linalg.norm(item_user, axis=1, keepdims=True)
    normalized = item_user / np.maximum(norms, 1e-8)

    similarity = (normalized @ normalized.T).astype(np.float32)
    np.fill_diagonal(similarity, 0.0)

    if 0 < neighbors < n_items:
        keep = np.argpartition(-similarity, neighbors, axis=1)[:, :neighbors]
        mask = np.zeros_like(similarity, dtype=bool)
        row_indices = np.arange(n_items)[:, None]
        mask[row_indices, keep] = True
        similarity = np.where(mask, similarity, 0.0).astype(np.float32)

    scores = np.empty((n_users, n_items), dtype=np.float32)
    for user_idx in range(n_users):
        seen = np.flatnonzero(user_item[user_idx])
        if len(seen) == 0:
            scores[user_idx] = 0.0
        else:
            scores[user_idx] = similarity[seen].mean(axis=0)
    return scores
