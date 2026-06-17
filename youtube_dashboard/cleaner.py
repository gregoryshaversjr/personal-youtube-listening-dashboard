"""Clean raw YouTube history records for analysis."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = ["title", "channel", "url", "watched_at", "content_type", "keyword_match"]
TIMEZONE_REPLACEMENTS = {
    " EDT": " -0400",
    " EST": " -0500",
    " CDT": " -0500",
    " CST": " -0600",
    " MDT": " -0600",
    " MST": " -0700",
    " PDT": " -0700",
    " PST": " -0800",
    " UTC": " +0000",
}


def clean_history(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Return a clean DataFrame with date helper columns."""
    df = raw_df.copy()
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df["title"] = df["title"].fillna("Untitled").astype(str).str.strip()
    df["channel"] = df["channel"].fillna("Unknown Channel").astype(str).str.strip()
    df["url"] = df["url"].fillna("").astype(str).str.strip()
    df["content_type"] = df["content_type"].fillna("YouTube").astype(str).str.strip()
    df["keyword_match"] = df["keyword_match"].fillna("").astype(str).str.strip()

    source_date = df["watched_at"] if "watched_at" in df.columns else df.get("watch_date", "")
    normalized_date = source_date.fillna("").astype(str)
    for label, offset in TIMEZONE_REPLACEMENTS.items():
        normalized_date = normalized_date.str.replace(label, offset, regex=False)
    parsed_dates = pd.to_datetime(
        normalized_date,
        format="%b %d, %Y, %I:%M:%S %p %z",
        errors="coerce",
        utc=True,
    )
    numeric_date = pd.to_numeric(source_date, errors="coerce")
    numeric_dates = pd.to_datetime(numeric_date, unit="ms", errors="coerce", utc=True)
    text_dates = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns, UTC]")
    needs_text_parse = parsed_dates.isna() & numeric_dates.isna()
    if needs_text_parse.any():
        text_dates.loc[needs_text_parse] = pd.to_datetime(
            source_date.loc[needs_text_parse],
            errors="coerce",
            utc=True,
        )
    fallback_dates = numeric_dates.fillna(text_dates)
    df["watched_at"] = parsed_dates.fillna(fallback_dates)
    df = df.dropna(subset=["watched_at"]).copy()
    df = df.sort_values("watched_at", ascending=False)

    local_time = df["watched_at"].dt.tz_convert("America/New_York")
    df["watch_date"] = local_time.dt.date
    df["watch_time"] = local_time.dt.strftime("%I:%M %p")
    df["month"] = local_time.dt.strftime("%Y-%m")
    df["day_of_week"] = local_time.dt.day_name()
    df["hour"] = local_time.dt.hour
    df["keyword_match"] = df["keyword_match"].where(df["keyword_match"] != "", df["title"])
    return df.reset_index(drop=True)


def filter_history(
    df: pd.DataFrame,
    keyword: str = "",
    channel: str = "All Channels",
    content_type: str = "All Types",
    start_date=None,
    end_date=None,
) -> pd.DataFrame:
    """Filter records by keyword, channel, type, and date range."""
    filtered = df.copy()
    if start_date is not None and end_date is not None:
        filtered = filtered[
            (pd.to_datetime(filtered["watch_date"]) >= pd.to_datetime(start_date))
            & (pd.to_datetime(filtered["watch_date"]) <= pd.to_datetime(end_date))
        ]
    if channel != "All Channels":
        filtered = filtered[filtered["channel"] == channel]
    if content_type != "All Types":
        filtered = filtered[filtered["content_type"] == content_type]
    if keyword.strip():
        term = keyword.strip().lower()
        title_match = filtered["title"].str.lower().str.contains(term, na=False)
        channel_match = filtered["channel"].str.lower().str.contains(term, na=False)
        filtered = filtered[title_match | channel_match]
    return filtered.reset_index(drop=True)
