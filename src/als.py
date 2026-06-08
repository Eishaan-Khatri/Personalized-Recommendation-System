"""Lightweight implicit ALS-style matrix factorization."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ALSModel:
    """User and item factors from alternating least-squares updates."""

    user_factors: np.ndarray
    item_factors: np.ndarray

    def score_all(self, batch_size: int = 1024) -> np.ndarray:
        n_users = self.user_factors.shape[0]
        n_items = self.item_factors.shape[0]
        scores = np.empty((n_users, n_items), dtype=np.float32)
        for start in range(0, n_users, batch_size):
            end = min(start + batch_size, n_users)
            scores[start:end] = self.user_factors[start:end] @ self.item_factors.T
        return scores


def _index_lists(frame: pd.DataFrame, group_col: str, value_col: str, size: int) -> list[np.ndarray]:
    grouped = frame.groupby(group_col)[value_col].apply(lambda values: np.array(values, dtype=np.int32))
    return [np.unique(grouped.get(idx, np.array([], dtype=np.int32))).astype(np.int32) for idx in range(size)]


def _solve_factor(other_factors: np.ndarray, indices: np.ndarray, regularization: float) -> np.ndarray:
    factors = other_factors[indices]
    if len(factors) == 0:
        return np.zeros(other_factors.shape[1], dtype=np.float32)
    lhs = factors.T @ factors
    lhs += regularization * np.eye(other_factors.shape[1], dtype=np.float32)
    rhs = factors.sum(axis=0)
    return np.linalg.solve(lhs, rhs).astype(np.float32)


def fit_implicit_als(
    train: pd.DataFrame,
    n_users: int,
    n_items: int,
    factors: int,
    epochs: int,
    regularization: float,
    seed: int,
) -> ALSModel:
    """Fit a compact implicit-feedback ALS model using positive interactions."""
    rng = np.random.default_rng(seed)
    user_factors = rng.normal(0.0, 0.04, size=(n_users, factors)).astype(np.float32)
    item_factors = rng.normal(0.0, 0.04, size=(n_items, factors)).astype(np.float32)

    user_items = _index_lists(train, "user_idx", "item_idx", n_users)
    item_users = _index_lists(train, "item_idx", "user_idx", n_items)

    for epoch in range(epochs):
        for user_idx, item_indices in enumerate(user_items):
            user_factors[user_idx] = _solve_factor(item_factors, item_indices, regularization)
        for item_idx, user_indices in enumerate(item_users):
            item_factors[item_idx] = _solve_factor(user_factors, user_indices, regularization)
        print(f"Finished ALS epoch {epoch + 1}/{epochs}")

    return ALSModel(user_factors=user_factors, item_factors=item_factors)
