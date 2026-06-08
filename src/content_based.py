"""Content-based recommendation from item genre features."""

from __future__ import annotations

import numpy as np

from .features import normalize_rows


def build_user_profiles(histories: list[np.ndarray], item_features: np.ndarray) -> np.ndarray:
    """Average metadata vectors for each user's positive-history items."""
    profiles = np.zeros((len(histories), item_features.shape[1]), dtype=np.float32)
    for user_idx, item_indices in enumerate(histories):
        if len(item_indices) == 0:
            continue
        profiles[user_idx] = item_features[item_indices].mean(axis=0)
    return normalize_rows(profiles)


def score_content_based(user_profiles: np.ndarray, item_features: np.ndarray) -> np.ndarray:
    """Score all user-item pairs by cosine similarity."""
    normalized_items = normalize_rows(item_features)
    return (user_profiles @ normalized_items.T).astype(np.float32)
