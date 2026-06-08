"""Baseline recommenders."""

from __future__ import annotations

import numpy as np
import pandas as pd


def popularity_vector(train: pd.DataFrame, n_items: int) -> np.ndarray:
    """Score items by log positive interaction count."""
    counts = np.bincount(train["item_idx"].to_numpy(dtype=np.int32), minlength=n_items).astype(np.float32)
    scores = np.log1p(counts)
    if scores.max() > 0:
        scores = scores / scores.max()
    return scores.astype(np.float32)


def popularity_score_matrix(popularity: np.ndarray, n_users: int) -> np.ndarray:
    """Repeat the popularity vector for every user."""
    return np.tile(popularity, (n_users, 1)).astype(np.float32)
