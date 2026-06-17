"""Project settings for the YouTube behavior dashboard."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

DEMO_DATA_PATH = DATA_DIR / "greg_demo_youtube_data.json"
SAMPLE_DATA_PATH = DATA_DIR / "sample_youtube_data.json"
DEMO_DATASET_NAME = "Greg's Demo YouTube Data"
SAMPLE_DATASET_NAME = "Sample YouTube Data"

DATE_COLUMN = "watch_date"
