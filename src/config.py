"""Project configuration."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
OUTPUT_DIR = ROOT_DIR / "outputs"
METRICS_DIR = OUTPUT_DIR / "metrics"
RECOMMENDATIONS_DIR = OUTPUT_DIR / "recommendations"
REPORTS_DIR = ROOT_DIR / "reports"

MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
MOVIELENS_DIR = RAW_DATA_DIR / "ml-1m"

RANDOM_SEED = 42
SEEDS = [11, 42, 73]
POSITIVE_RATING_THRESHOLD = 4
TOP_K = 10
CANDIDATE_K = 200
SAMPLED_NEGATIVES = 100

FACTORS = 32
EPOCHS = 1
LEARNING_RATE = 0.045
REGULARIZATION = 0.002
ALS_FACTORS = 24
ALS_EPOCHS = 2
ALS_REGULARIZATION = 0.08
ITEMKNN_NEIGHBORS = 80

HYBRID_WEIGHTS = {
    "collaborative": 0.55,
    "content": 0.30,
    "popularity": 0.15,
}

RANKER_WEIGHT_GRID = [
    {
        "name": "balanced_retrieval",
        "bpr": 0.30,
        "als": 0.25,
        "itemknn": 0.20,
        "content": 0.10,
        "popularity": 0.10,
        "novelty": 0.05,
    },
    {
        "name": "coverage_aware",
        "bpr": 0.25,
        "als": 0.20,
        "itemknn": 0.15,
        "content": 0.15,
        "popularity": 0.05,
        "novelty": 0.20,
    },
    {
        "name": "behavior_heavy",
        "bpr": 0.40,
        "als": 0.30,
        "itemknn": 0.15,
        "content": 0.05,
        "popularity": 0.05,
        "novelty": 0.05,
    },
    {
        "name": "content_safety",
        "bpr": 0.20,
        "als": 0.20,
        "itemknn": 0.15,
        "content": 0.25,
        "popularity": 0.05,
        "novelty": 0.15,
    },
]


def ensure_output_dirs() -> None:
    """Create output directories used by the pipeline."""
    for path in [RAW_DATA_DIR, METRICS_DIR, RECOMMENDATIONS_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
