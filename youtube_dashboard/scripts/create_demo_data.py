"""Create the demo JSON dataset from extracted YouTube Takeout history."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cleaner import clean_history
from config import DEMO_DATA_PATH
from data_loader import dataframe_to_json_records, load_takeout_history_files


TAKEOUT_HISTORY_DIR = (
    ROOT.parent
    / "work"
    / "takeout_subset"
    / "Takeout"
    / "YouTube and YouTube Music"
    / "history"
)


def main() -> None:
    """Build a right-sized demo data file for the dashboard."""
    paths = [
        TAKEOUT_HISTORY_DIR / "watch-history.html",
        TAKEOUT_HISTORY_DIR / "search-history.html",
    ]
    raw_df = load_takeout_history_files(paths)
    clean_df = clean_history(raw_df)
    DEMO_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEMO_DATA_PATH.write_text(dataframe_to_json_records(clean_df), encoding="utf-8")
    print(f"Wrote {len(clean_df)} demo records to {DEMO_DATA_PATH}")


if __name__ == "__main__":
    main()
