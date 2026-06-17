"""Analyze cleaned YouTube history data."""

from __future__ import annotations

import pandas as pd


DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def summary_metrics(df: pd.DataFrame) -> dict[str, str | int]:
    """Calculate the headline dashboard numbers."""
    if df.empty:
        return {
            "total_records": 0,
            "top_channel": "None",
            "most_active_day": "None",
            "date_range": "No records",
        }
    date_range = f"{df['watch_date'].min()} to {df['watch_date'].max()}"
    return {
        "total_records": len(df),
        "top_channel": top_channels(df, 1).index[0],
        "most_active_day": activity_by_day(df).idxmax(),
        "date_range": date_range,
    }


def top_channels(df: pd.DataFrame, limit: int = 10) -> pd.Series:
    """Return the most frequent channels."""
    if df.empty:
        return pd.Series(dtype="int64")
    return df["channel"].value_counts().head(limit)


def top_titles(df: pd.DataFrame, limit: int = 10) -> pd.Series:
    """Return the most repeated titles or searches."""
    if df.empty:
        return pd.Series(dtype="int64")
    return df["title"].value_counts().head(limit)


def activity_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """Count records for each calendar date."""
    if df.empty:
        return pd.DataFrame(columns=["watch_date", "records"])
    return df.groupby("watch_date").size().reset_index(name="records").sort_values("watch_date")


def activity_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Count records by month."""
    if df.empty:
        return pd.DataFrame(columns=["month", "records"])
    return df.groupby("month").size().reset_index(name="records").sort_values("month")


def activity_by_day(df: pd.DataFrame) -> pd.Series:
    """Count records by day of week in natural order."""
    if df.empty:
        return pd.Series(dtype="int64")
    counts = df["day_of_week"].value_counts()
    return counts.reindex(DAY_ORDER, fill_value=0)


def activity_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """Count records by hour of day."""
    if df.empty:
        return pd.DataFrame(columns=["hour", "records"])
    hourly = df.groupby("hour").size().reset_index(name="records")
    all_hours = pd.DataFrame({"hour": list(range(24))})
    return all_hours.merge(hourly, how="left", on="hour").fillna(0)
