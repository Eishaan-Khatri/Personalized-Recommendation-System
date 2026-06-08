"""Implicit-feedback collaborative filtering."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class MatrixFactorizationModel:
    """User and item embeddings trained with pairwise ranking updates."""

    user_factors: np.ndarray
    item_factors: np.ndarray

    def score_all(self, batch_size: int = 1024) -> np.ndarray:
        """Return dense user-item scores."""
        n_users = self.user_factors.shape[0]
        n_items = self.item_factors.shape[0]
        scores = np.empty((n_users, n_items), dtype=np.float32)
        for start in range(0, n_users, batch_size):
            end = min(start + batch_size, n_users)
            scores[start:end] = self.user_factors[start:end] @ self.item_factors.T
        return scores


def fit_bpr_matrix_factorization(
    train: pd.DataFrame,
    history_sets: list[set[int]],
    n_users: int,
    n_items: int,
    factors: int,
    epochs: int,
    learning_rate: float,
    regularization: float,
    seed: int,
) -> MatrixFactorizationModel:
    """Train a small implicit-feedback matrix factorization model."""
    rng = np.random.default_rng(seed)
    user_factors = rng.normal(0.0, 0.05, size=(n_users, factors)).astype(np.float32)
    item_factors = rng.normal(0.0, 0.05, size=(n_items, factors)).astype(np.float32)

    interactions = train[["user_idx", "item_idx"]].drop_duplicates().to_numpy(dtype=np.int32)
    order = np.arange(len(interactions))

    for epoch in range(epochs):
        rng.shuffle(order)
        for row_idx in order:
            user_idx = int(interactions[row_idx, 0])
            pos_item = int(interactions[row_idx, 1])
            seen = history_sets[user_idx]

            neg_item = int(rng.integers(n_items))
            while neg_item in seen:
                neg_item = int(rng.integers(n_items))

            user_vec = user_factors[user_idx].copy()
            pos_vec = item_factors[pos_item].copy()
            neg_vec = item_factors[neg_item].copy()

            x_uij = float(user_vec @ (pos_vec - neg_vec))
            grad = 1.0 / (1.0 + np.exp(x_uij))

            user_factors[user_idx] += learning_rate * (
                grad * (pos_vec - neg_vec) - regularization * user_vec
            )
            item_factors[pos_item] += learning_rate * (
                grad * user_vec - regularization * pos_vec
            )
            item_factors[neg_item] += learning_rate * (
                -grad * user_vec - regularization * neg_vec
            )

        print(f"Finished matrix factorization epoch {epoch + 1}/{epochs}")

    return MatrixFactorizationModel(user_factors=user_factors, item_factors=item_factors)
