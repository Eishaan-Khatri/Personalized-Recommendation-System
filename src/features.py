"""Feature builders for item metadata."""

from __future__ import annotations

import numpy as np
import pandas as pd


def build_genre_matrix(items: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    """Build a binary item-genre matrix from pipe-separated genre strings."""
    genres = sorted({genre for value in items["genres"] for genre in str(value).split("|")})
    matrix = np.zeros((len(items), len(genres)), dtype=np.float32)
    genre_to_idx = {genre: idx for idx, genre in enumerate(genres)}

    for row in items.itertuples(index=False):
        item_idx = int(row.item_idx)
        for genre in str(row.genres).split("|"):
            matrix[item_idx, genre_to_idx[genre]] = 1.0
    return matrix, genres


def normalize_rows(matrix: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """L2-normalize rows in a dense matrix."""
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.maximum(norms, eps)


def minmax_rows(scores: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """Min-max normalize each user score row."""
    row_min = scores.min(axis=1, keepdims=True)
    row_max = scores.max(axis=1, keepdims=True)
    return (scores - row_min) / np.maximum(row_max - row_min, eps)
