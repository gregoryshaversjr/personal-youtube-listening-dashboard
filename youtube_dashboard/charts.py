"""Interactive dashboard charts built with Altair."""

from __future__ import annotations

import altair as alt
import pandas as pd


TEAL = "#0B7A75"
CORAL = "#FF6B35"
GOLD = "#FF6B35"
INK = "#252525"
MUTED = "#5f6f75"
GRID = "#d7e2e6"


def activity_date_chart(df: pd.DataFrame) -> alt.Chart:
    """Create a zoomable line chart for activity by date."""
    chart_df = df.copy()
    chart_df["watch_date"] = pd.to_datetime(chart_df["watch_date"])
    zoom = alt.selection_interval(bind="scales", encodings=["x"])
    return (
        alt.Chart(chart_df)
        .mark_line(point=alt.OverlayMarkDef(size=70, filled=True), color=CORAL, strokeWidth=3)
        .encode(
            x=alt.X("watch_date:T", title="Date"),
            y=alt.Y("records:Q", title="Records"),
            tooltip=[
                alt.Tooltip("watch_date:T", title="Date", format="%b %d, %Y"),
                alt.Tooltip("records:Q", title="Records"),
            ],
        )
        .add_params(zoom)
        .properties(height=280)
        .configure(background="transparent")
        .configure_axis(labelColor=MUTED, titleColor=INK, gridColor=GRID)
        .configure_view(strokeWidth=0)
    )


def vertical_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    x_title: str,
    y_title: str,
    color: str | None = None,
) -> alt.Chart:
    """Create a vertical bar chart with hover highlighting."""
    hover = alt.selection_point(on="pointerover", empty=False)
    bar_color = color or TEAL
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X(f"{x_column}:N", title=x_title, sort=None),
            y=alt.Y(f"{y_column}:Q", title=y_title),
            color=alt.condition(hover, alt.value(CORAL), alt.value(bar_color)),
            tooltip=[
                alt.Tooltip(f"{x_column}:N", title=x_title),
                alt.Tooltip(f"{y_column}:Q", title=y_title),
            ],
        )
        .add_params(hover)
        .properties(height=280)
        .configure(background="transparent")
        .configure_axis(labelColor=MUTED, titleColor=INK, gridColor=GRID)
        .configure_view(strokeWidth=0)
    )


def series_bar_chart(
    series: pd.Series,
    name_column: str,
    count_column: str = "records",
) -> alt.Chart:
    """Create a horizontal bar chart from a Pandas Series."""
    chart_df = series.rename(count_column).reset_index()
    chart_df.columns = [name_column, count_column]
    hover = alt.selection_point(on="pointerover", empty=False)
    return (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            x=alt.X(f"{count_column}:Q", title="Records"),
            y=alt.Y(f"{name_column}:N", title=None, sort="-x"),
            color=alt.condition(hover, alt.value(CORAL), alt.value(TEAL)),
            tooltip=[
                alt.Tooltip(f"{name_column}:N", title=name_column.replace("_", " ").title()),
                alt.Tooltip(f"{count_column}:Q", title="Records"),
            ],
        )
        .add_params(hover)
        .properties(height=380)
        .configure(background="transparent")
        .configure_axis(labelColor=MUTED, titleColor=INK, gridColor=GRID)
        .configure_view(strokeWidth=0)
    )
