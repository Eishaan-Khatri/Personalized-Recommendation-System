"""Train/test preparation for recommendation evaluation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import POSITIVE_RATING_THRESHOLD


def build_holdout_split(
    ratings: pd.DataFrame,
    min_positive_interactions: int = 2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Use each eligible user's latest positive event as the held-out item."""
    positive = ratings[ratings["rating"] >= POSITIVE_RATING_THRESHOLD].copy()
    positive = positive.sort_values(["user_idx", "timestamp"])

    counts = positive.groupby("user_idx")["item_idx"].size()
    eligible_users = counts[counts >= min_positive_interactions].index
    eligible = positive[positive["user_idx"].isin(eligible_users)].copy()

    test_idx = eligible.groupby("user_idx").tail(1).index
    test = eligible.loc[test_idx, ["user_idx", "user_id", "item_idx", "item_id"]].copy()
    train = positive.drop(index=test_idx).copy()
    return train, test.reset_index(drop=True)


def build_validation_test_split(
    ratings: pd.DataFrame,
    min_positive_interactions: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Use each eligible user's second-latest and latest positives as val/test."""
    positive = ratings[ratings["rating"] >= POSITIVE_RATING_THRESHOLD].copy()
    positive = positive.sort_values(["user_idx", "timestamp"])

    counts = positive.groupby("user_idx")["item_idx"].size()
    eligible_users = counts[counts >= min_positive_interactions].index
    eligible = positive[positive["user_idx"].isin(eligible_users)].copy()

    latest_two = eligible.groupby("user_idx").tail(2)
    validation_idx = latest_two.groupby("user_idx").head(1).index
    test_idx = latest_two.groupby("user_idx").tail(1).index

    columns = ["user_idx", "user_id", "item_idx", "item_id"]
    validation = eligible.loc[validation_idx, columns].copy().reset_index(drop=True)
    test = eligible.loc[test_idx, columns].copy().reset_index(drop=True)
    train = positive.drop(index=validation_idx.union(test_idx)).copy()
    return train.reset_index(drop=True), validation, test


def build_user_histories(train: pd.DataFrame, n_users: int) -> list[np.ndarray]:
    """Return train item indices for each user."""
    histories: list[np.ndarray] = []
    grouped = train.groupby("user_idx")["item_idx"].apply(lambda values: np.array(values, dtype=np.int32))
    for user_idx in range(n_users):
        values = grouped.get(user_idx)
        if values is None:
            histories.append(np.array([], dtype=np.int32))
        else:
            histories.append(np.unique(values).astype(np.int32))
    return histories


def build_user_history_sets(histories: list[np.ndarray]) -> list[set[int]]:
    """Return set histories for fast membership checks."""
    return [set(map(int, items)) for items in histories]
