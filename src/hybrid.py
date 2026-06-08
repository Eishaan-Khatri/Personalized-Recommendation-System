"""Hybrid recommendation scoring."""

from __future__ import annotations

import numpy as np

from .features import minmax_rows


def build_hybrid_scores(
    collaborative_scores: np.ndarray,
    content_scores: np.ndarray,
    popularity_scores: np.ndarray,
    weights: dict[str, float],
) -> np.ndarray:
    """Combine collaborative, content, and popularity scores."""
    collaborative_norm = minmax_rows(collaborative_scores)
    content_norm = minmax_rows(content_scores)
    popularity_norm = popularity_scores.astype(np.float32)
    return (
        weights["collaborative"] * collaborative_norm
        + weights["content"] * content_norm
        + weights["popularity"] * popularity_norm
    ).astype(np.float32)
