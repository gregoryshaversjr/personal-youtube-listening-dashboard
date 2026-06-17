"""Generate written observations from dashboard data."""

from __future__ import annotations

import pandas as pd

from analyzer import activity_by_day, activity_by_hour, top_channels, top_titles


def generate_insights(df: pd.DataFrame) -> list[str]:
    """Create short beginner-friendly insights from the filtered data."""
    if df.empty:
        return ["No records match the current filters."]

    insights = []
    channels = top_channels(df, 3)
    titles = top_titles(df, 3)
    days = activity_by_day(df)
    hours = activity_by_hour(df)

    if not channels.empty:
        channel_name = channels.index[0]
        insights.append(f"Your top channel in this view is {channel_name} with {channels.iloc[0]} records.")
    if not titles.empty:
        insights.append(f"Your most repeated title or search is: {titles.index[0]}.")
    if not days.empty:
        insights.append(f"Your most active day of the week is {days.idxmax()}.")
    if not hours.empty:
        busiest_hour = int(hours.sort_values("records", ascending=False).iloc[0]["hour"])
        insights.append(f"Your busiest hour is around {busiest_hour:02d}:00.")
    if df["content_type"].nunique() > 1:
        mix = df["content_type"].value_counts().to_dict()
        insights.append(f"This filtered view contains a mix of activity types: {mix}.")
    return insights
