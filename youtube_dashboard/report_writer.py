"""Save cleaned data and summary reports."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analyzer import summary_metrics, top_channels
from config import OUTPUT_DIR
from insights import generate_insights


def save_cleaned_csv(df: pd.DataFrame, path: Path | None = None) -> Path:
    """Save the cleaned records to a CSV file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = path or OUTPUT_DIR / "cleaned_history.csv"
    df.to_csv(target, index=False)
    return target


def save_summary_report(df: pd.DataFrame, path: Path | None = None) -> Path:
    """Save a plain text report with metrics, top channels, and insights."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = path or OUTPUT_DIR / "summary_report.txt"
    metrics = summary_metrics(df)
    lines = [
        "Personal YouTube Listening Behavior Dashboard Report",
        "",
        f"Total records: {metrics['total_records']}",
        f"Top channel: {metrics['top_channel']}",
        f"Most active day: {metrics['most_active_day']}",
        f"Date range: {metrics['date_range']}",
        "",
        "Top channels:",
    ]
    for channel, count in top_channels(df, 10).items():
        lines.append(f"- {channel}: {count}")
    lines.extend(["", "Insights:"])
    lines.extend(f"- {insight}" for insight in generate_insights(df))
    target.write_text("\n".join(lines), encoding="utf-8")
    return target
