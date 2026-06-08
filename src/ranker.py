"""Two-stage candidate generation and hybrid re-ranking."""

from __future__ import annotations

import numpy as np

from .evaluation import top_k_for_user
from .features import minmax_rows


def build_candidate_mask(
    retrieval_scores: list[np.ndarray],
    histories: list[np.ndarray],
    candidate_k: int,
) -> np.ndarray:
    """Union top candidates from multiple retrieval models."""
    n_users, n_items = retrieval_scores[0].shape
    mask = np.zeros((n_users, n_items), dtype=bool)

    for scores in retrieval_scores:
        for user_idx in range(n_users):
            user_scores = scores[user_idx].copy()
            seen = histories[user_idx]
            if len(seen) > 0:
                user_scores[seen] = -np.inf
            top_items = top_k_for_user(user_scores, candidate_k)
            mask[user_idx, top_items] = True
    return mask


def build_ranker_components(
    bpr_scores: np.ndarray,
    als_scores: np.ndarray,
    itemknn_scores: np.ndarray,
    content_scores: np.ndarray,
    popularity_scores: np.ndarray,
) -> dict[str, np.ndarray]:
    """Normalize component score matrices for the re-ranker."""
    popularity = popularity_scores.astype(np.float32)
    novelty = 1.0 - popularity
    return {
        "bpr": minmax_rows(bpr_scores),
        "als": minmax_rows(als_scores),
        "itemknn": minmax_rows(itemknn_scores),
        "content": minmax_rows(content_scores),
        "popularity": popularity,
        "novelty": novelty,
    }


def combine_components(components: dict[str, np.ndarray], weights: dict[str, float]) -> np.ndarray:
    """Blend normalized score components."""
    score = np.zeros_like(next(iter(components.values())), dtype=np.float32)
    for key, weight in weights.items():
        if key == "name":
            continue
        score += float(weight) * components[key]
    return score.astype(np.float32)


def apply_candidate_mask(scores: np.ndarray, candidate_mask: np.ndarray) -> np.ndarray:
    """Keep only stage-one candidates for final re-ranking."""
    return np.where(candidate_mask, scores, -np.inf).astype(np.float32)
