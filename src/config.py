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
POSITIVE_RATING_THRESHOLD = 4
TOP_K = 10

FACTORS = 32
EPOCHS = 1
LEARNING_RATE = 0.045
REGULARIZATION = 0.002

HYBRID_WEIGHTS = {
    "collaborative": 0.55,
    "content": 0.30,
    "popularity": 0.15,
}


def ensure_output_dirs() -> None:
    """Create output directories used by the pipeline."""
    for path in [RAW_DATA_DIR, METRICS_DIR, RECOMMENDATIONS_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
