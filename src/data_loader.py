"""Data loading helpers for MovieLens 1M."""

from __future__ import annotations

import shutil
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

from .config import MOVIELENS_DIR, MOVIELENS_URL, RAW_DATA_DIR


def download_movielens_1m() -> None:
    """Download and extract MovieLens 1M if it is not already present."""
    ratings_path = MOVIELENS_DIR / "ratings.dat"
    movies_path = MOVIELENS_DIR / "movies.dat"
    if ratings_path.exists() and movies_path.exists():
        return

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = RAW_DATA_DIR / "ml-1m.zip"
    print(f"Downloading MovieLens 1M from {MOVIELENS_URL}")
    with urllib.request.urlopen(MOVIELENS_URL) as response:
        with archive_path.open("wb") as file:
            shutil.copyfileobj(response, file)

    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(RAW_DATA_DIR)


def load_movielens_1m() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load ratings and movie metadata with contiguous internal ids."""
    download_movielens_1m()

    ratings = pd.read_csv(
        MOVIELENS_DIR / "ratings.dat",
        sep="::",
        engine="python",
        names=["user_id", "item_id", "rating", "timestamp"],
        encoding="latin-1",
    )
    items = pd.read_csv(
        MOVIELENS_DIR / "movies.dat",
        sep="::",
        engine="python",
        names=["item_id", "title", "genres"],
        encoding="latin-1",
    )

    user_lookup = (
        pd.DataFrame({"user_id": sorted(ratings["user_id"].unique())})
        .reset_index()
        .rename(columns={"index": "user_idx"})
    )
    item_lookup = (
        pd.DataFrame({"item_id": sorted(items["item_id"].unique())})
        .reset_index()
        .rename(columns={"index": "item_idx"})
    )

    ratings = ratings.merge(user_lookup, on="user_id", how="left")
    ratings = ratings.merge(item_lookup, on="item_id", how="left")
    items = items.merge(item_lookup, on="item_id", how="left")
    items = items.sort_values("item_idx").reset_index(drop=True)
    ratings = ratings.sort_values(["user_idx", "timestamp"]).reset_index(drop=True)
    return ratings, items
