"""Batch top-K recommendation generation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluation import top_k_for_user


def build_recommendation_table(
    model_name: str,
    scores: np.ndarray,
    histories: list[np.ndarray],
    items: pd.DataFrame,
    user_lookup: pd.DataFrame,
    sample_user_count: int,
    k: int,
) -> pd.DataFrame:
    """Generate a readable top-K recommendation table for sample users."""
    rows: list[dict[str, object]] = []
    sample_users = user_lookup["user_idx"].head(sample_user_count).to_numpy(dtype=np.int32)
    item_lookup = items.set_index("item_idx")
    user_id_lookup = user_lookup.set_index("user_idx")["user_id"].to_dict()

    for user_idx in sample_users:
        user_scores = scores[int(user_idx)].copy()
        seen = histories[int(user_idx)]
        if len(seen) > 0:
            user_scores[seen] = -np.inf
        top_items = top_k_for_user(user_scores, k)
        for rank, item_idx in enumerate(top_items, start=1):
            item = item_lookup.loc[int(item_idx)]
            rows.append(
                {
                    "model": model_name,
                    "user_id": int(user_id_lookup[int(user_idx)]),
                    "rank": rank,
                    "item_id": int(item["item_id"]),
                    "title": item["title"],
                    "genres": item["genres"],
                    "score": float(user_scores[int(item_idx)]),
                }
            )
    return pd.DataFrame(rows)
