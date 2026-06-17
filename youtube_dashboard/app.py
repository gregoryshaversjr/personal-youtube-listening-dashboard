"""Streamlit app for exploring YouTube listening and viewing behavior."""

from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st

from analyzer import (
    activity_by_date,
    activity_by_day,
    activity_by_hour,
    activity_by_month,
    summary_metrics,
    top_channels,
    top_titles,
)
from charts import activity_date_chart, series_bar_chart, vertical_bar_chart
from cleaner import clean_history, filter_history
from data_loader import get_demo_dataset_name, load_demo_data, load_uploaded_files
from insights import generate_insights
from report_writer import save_cleaned_csv, save_summary_report


st.set_page_config(
    page_title="YouTube Listening Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    """Add a small custom theme to make the dashboard feel polished."""
    st.markdown(
        """
        <style>
        :root {
            --page: #FFFFFF;
            --ink: #252525;
            --muted: #5f6f75;
            --panel: #FFFFFF;
            --sidebar: #FFFFFF;
            --line: #d7e2e6;
            --teal: #0B7A75;
            --coral: #FF6B35;
            --gold: #FF6B35;
            --pill-bg: #eef7f9;
            --pill-line: #c8dce2;
            --tab-bg: #f7fbfc;
            --shadow: rgba(11, 122, 117, 0.10);
        }

        .stApp {
            background: var(--page);
            color: var(--ink);
        }

        header[data-testid="stHeader"] {
            background: var(--page);
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            color: var(--teal);
        }

        [data-testid="collapsedControl"] {
            background: var(--teal) !important;
            border: 2px solid var(--teal) !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 22px rgba(11, 122, 117, 0.26) !important;
            left: .65rem !important;
            top: .65rem !important;
            width: 42px !important;
            height: 42px !important;
            opacity: 1 !important;
            z-index: 999999 !important;
        }

        [data-testid="collapsedControl"] button {
            background: var(--teal) !important;
            border: 2px solid var(--teal) !important;
            border-radius: 10px !important;
            min-width: 42px !important;
            width: 42px !important;
            height: 42px !important;
            padding: 0 !important;
            opacity: 1 !important;
        }

        [data-testid="collapsedControl"] button svg,
        [data-testid="collapsedControl"] svg {
            color: #FFFFFF !important;
            fill: currentColor !important;
            stroke: currentColor !important;
            width: 26px !important;
            height: 26px !important;
            opacity: 1 !important;
        }

        [data-testid="collapsedControl"] svg path {
            fill: currentColor !important;
            stroke: currentColor !important;
        }

        [data-testid="collapsedControl"]:hover,
        [data-testid="collapsedControl"] button:hover {
            background: var(--coral) !important;
            border-color: var(--coral) !important;
        }

        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"] {
            background: var(--teal) !important;
            border: 2px solid var(--teal) !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 22px rgba(11, 122, 117, 0.26) !important;
            color: #FFFFFF !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            opacity: 1 !important;
            min-width: 42px !important;
            width: 42px !important;
            height: 42px !important;
            padding: 0 !important;
            z-index: 999999 !important;
        }

        [data-testid="stExpandSidebarButton"] {
            position: fixed !important;
            left: .65rem !important;
            top: .65rem !important;
        }

        [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
        [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
        [data-testid="stExpandSidebarButton"] span,
        [data-testid="stSidebarCollapseButton"] span {
            color: #FFFFFF !important;
            display: none !important;
            font-size: 0 !important;
            line-height: 1 !important;
            opacity: 1 !important;
        }

        [data-testid="stExpandSidebarButton"]::after,
        [data-testid="stSidebarCollapseButton"]::after {
            content: "☰";
            color: #FFFFFF !important;
            display: block;
            font-size: 24px;
            font-weight: 800;
            line-height: 1;
            margin: 0;
            transform: translateY(-1px);
        }

        [data-testid="stExpandSidebarButton"]:hover,
        [data-testid="stSidebarCollapseButton"]:hover {
            background: var(--coral) !important;
            border-color: var(--coral) !important;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar);
            border-right: 1px solid var(--line);
            box-shadow: 8px 0 24px rgba(11, 122, 117, 0.06);
        }

        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p {
            color: var(--ink);
        }

        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] small {
            color: var(--ink) !important;
        }

        [data-testid="stSidebar"] svg {
            color: var(--teal) !important;
            fill: currentColor !important;
        }

        [data-testid="stSidebar"] svg path {
            fill: currentColor !important;
            stroke: currentColor !important;
        }

        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] [data-baseweb="base-input"],
        [data-testid="stSidebar"] [data-baseweb="base-input"] > div,
        [data-testid="stSidebar"] [data-baseweb="select"],
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
            background: var(--panel) !important;
            border-color: var(--line) !important;
            color: var(--ink) !important;
        }

        [data-testid="stSidebar"] [data-baseweb="base-input"]:focus-within,
        [data-testid="stSidebar"] [data-baseweb="select"]:focus-within {
            background: var(--panel) !important;
            border-color: var(--teal) !important;
            box-shadow: 0 0 0 1px var(--teal) !important;
        }

        [data-baseweb="popover"],
        [data-baseweb="popover"] ul,
        [role="listbox"] {
            background: var(--panel) !important;
            color: var(--ink) !important;
        }

        [data-testid="stSidebar"] button {
            background: var(--teal) !important;
            border-color: var(--teal) !important;
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] button:hover {
            background: var(--coral) !important;
            border-color: var(--coral) !important;
            color: #ffffff !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        div[data-testid="stMetric"],
        div[data-testid="stDataFrame"],
        div[data-testid="stChart"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 8px 20px var(--shadow);
        }

        div[data-testid="stMetric"] label {
            color: var(--muted);
            font-weight: 700;
        }

        div[data-testid="stMetricValue"] {
            color: var(--ink);
            font-weight: 800;
        }

        .dashboard-hero {
            background: var(--panel);
            border: 1px solid var(--line);
            border-left: 6px solid var(--coral);
            border-radius: 8px;
            padding: 1.25rem 1.35rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 10px 24px var(--shadow);
        }

        .dashboard-hero h1 {
            color: var(--ink);
            font-size: 2.1rem;
            line-height: 1.15;
            margin: 0 0 .45rem 0;
            letter-spacing: 0;
        }

        .dashboard-hero p {
            color: var(--muted);
            font-size: 1rem;
            margin: 0;
        }

        .dataset-pill {
            display: inline-block;
            background: var(--pill-bg);
            color: var(--teal);
            border: 1px solid var(--pill-line);
            border-radius: 999px;
            padding: .28rem .7rem;
            font-size: .82rem;
            font-weight: 700;
            margin-top: .85rem;
        }

        .section-label {
            color: var(--teal);
            font-size: .8rem;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin: 1.2rem 0 .35rem 0;
        }

        .pretty-subhead {
            color: var(--ink);
            font-size: 1.22rem;
            font-weight: 800;
            margin: 0 0 .7rem 0;
        }

        .insight-list {
            background: var(--panel);
            border: 1px solid var(--line);
            border-left: 5px solid var(--teal);
            border-radius: 8px;
            padding: 1rem 1.15rem;
            box-shadow: 0 8px 20px var(--shadow);
        }

        .insight-item {
            color: var(--ink);
            margin: .35rem 0;
            line-height: 1.45;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: .35rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: var(--tab-bg);
            border: 1px solid var(--line);
            border-radius: 8px 8px 0 0;
            padding: .65rem 1rem;
        }

        .stTabs [aria-selected="true"] {
            background: var(--panel);
            color: var(--coral);
            border-bottom: 2px solid var(--coral);
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 8px;
            border: 1px solid var(--teal);
            color: #ffffff;
            background: var(--teal);
            font-weight: 700;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: var(--coral);
            color: #ffffff;
            background: var(--coral);
        }

        .stSelectbox [data-baseweb="select"],
        .stTextInput input,
        .stDateInput input {
            background: var(--panel);
            color: var(--ink);
            border-color: var(--line);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str) -> None:
    """Render a small section label."""
    st.markdown(f"<div class='section-label'>{text}</div>", unsafe_allow_html=True)


def subhead(text: str) -> None:
    """Render a compact polished subheading."""
    st.markdown(f"<div class='pretty-subhead'>{text}</div>", unsafe_allow_html=True)


inject_styles()


@st.cache_data
def get_demo_data() -> pd.DataFrame:
    """Load and clean the demo data once."""
    return clean_history(load_demo_data())


def reset_to_demo() -> None:
    """Reset Streamlit session state to the built-in dataset."""
    st.session_state["clean_df"] = get_demo_data()
    st.session_state["dataset_name"] = get_demo_dataset_name()
    st.session_state["profile_name"] = "Greg"
    st.session_state["upload_summary"] = ""


if "clean_df" not in st.session_state:
    reset_to_demo()

with st.sidebar:
    st.header("Dashboard Controls")
    profile_name = st.text_input("Temporary profile name", st.session_state.get("profile_name", "Greg"))
    st.session_state["profile_name"] = profile_name

    uploaded_files = st.file_uploader(
        "Upload YouTube history files",
        type=["json", "csv", "html", "htm", "zip", "tgz", "gz"],
        accept_multiple_files=True,
        help="Upload watch-history.html, search-history.html, a cleaned CSV/JSON file, or a YouTube Takeout ZIP/TGZ archive.",
    )
    st.caption("Large Takeout archives can be too big for the uploader. For those, upload the history HTML files directly.")

    if uploaded_files:
        file_names = ", ".join(uploaded_file.name for uploaded_file in uploaded_files)
        st.caption(f"Ready to format: {file_names}")

    if st.button("Clean and process upload", disabled=not uploaded_files):
        try:
            with st.spinner("Formatting uploaded YouTube data..."):
                raw_upload = load_uploaded_files(uploaded_files)
                clean_upload = clean_history(raw_upload)
            st.session_state["clean_df"] = clean_upload
            st.session_state["dataset_name"] = f"{profile_name or 'Uploaded'} Upload"
            st.session_state["upload_summary"] = (
                f"Formatted {len(raw_upload):,} raw records into {len(clean_upload):,} clean dashboard rows."
            )
            st.success("Uploaded data cleaned and processed.")
        except Exception as exc:
            st.error(f"Could not load file: {exc}")

    if st.session_state.get("upload_summary"):
        st.info(st.session_state["upload_summary"])

    if st.button("Reset to demo data"):
        reset_to_demo()
        st.rerun()

df = st.session_state["clean_df"]
dataset_name = escape(st.session_state["dataset_name"])
st.markdown(
    f"""
    <div class="dashboard-hero">
        <h1>Personal YouTube Listening Behavior Dashboard</h1>
        <p>A clean view of your YouTube watching, searching, and listening habits.</p>
        <span class="dataset-pill">Current dataset: {dataset_name}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("No usable records were found.")
    st.stop()

min_date = df["watch_date"].min()
max_date = df["watch_date"].max()

with st.sidebar:
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    channels = ["All Channels"] + sorted(df["channel"].dropna().unique().tolist())
    selected_channel = st.selectbox("Channel", channels)
    types = ["All Types"] + sorted(df["content_type"].dropna().unique().tolist())
    selected_type = st.selectbox("Activity type", types)
    keyword = st.text_input("Keyword search")

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered_df = filter_history(
    df,
    keyword=keyword,
    channel=selected_channel,
    content_type=selected_type,
    start_date=start_date,
    end_date=end_date,
)

metrics = summary_metrics(filtered_df)
section_label("Snapshot")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", metrics["total_records"])
col2.metric("Top Channel", metrics["top_channel"])
col3.metric("Most Active Day", metrics["most_active_day"])
col4.metric("Date Range", metrics["date_range"])

if filtered_df.empty:
    st.info("No records match the current filters.")
    st.stop()

tab_overview, tab_channels, tab_records, tab_export = st.tabs(
    ["Overview", "Channels & Titles", "Records", "Export"]
)

with tab_overview:
    left, right = st.columns(2)
    with left:
        section_label("Trends")
        subhead("Activity Over Time")
        st.altair_chart(activity_date_chart(activity_by_date(filtered_df)), width="stretch")
        subhead("Activity by Month")
        st.altair_chart(
            vertical_bar_chart(activity_by_month(filtered_df), "month", "records", "Month", "Records"),
            width="stretch",
        )
    with right:
        section_label("Rhythm")
        subhead("Activity by Day")
        st.altair_chart(series_bar_chart(activity_by_day(filtered_df), "day_of_week"), width="stretch")
        subhead("Activity by Hour")
        hourly_df = activity_by_hour(filtered_df)
        hourly_df["hour"] = hourly_df["hour"].astype(int).astype(str).str.zfill(2) + ":00"
        st.altair_chart(
            vertical_bar_chart(hourly_df, "hour", "records", "Hour", "Records", color="#FF6B35"),
            width="stretch",
        )

    section_label("Insights")
    insight_html = "".join(
        f"<div class='insight-item'>{escape(insight)}</div>" for insight in generate_insights(filtered_df)
    )
    st.markdown(f"<div class='insight-list'>{insight_html}</div>", unsafe_allow_html=True)

with tab_channels:
    left, right = st.columns(2)
    with left:
        section_label("Channels")
        subhead("Top Channels")
        st.altair_chart(series_bar_chart(top_channels(filtered_df, 15), "channel"), width="stretch")
    with right:
        section_label("Titles")
        subhead("Top Titles or Searches")
        st.dataframe(top_titles(filtered_df, 15).rename("records"), width="stretch")

with tab_records:
    section_label("Table")
    subhead("Cleaned Records")
    columns = ["title", "channel", "content_type", "watch_date", "watch_time", "url"]
    st.dataframe(filtered_df[columns], width="stretch", hide_index=True)

with tab_export:
    section_label("Output")
    subhead("Save Results")
    if st.button("Save cleaned CSV and summary report"):
        csv_path = save_cleaned_csv(filtered_df)
        report_path = save_summary_report(filtered_df)
        st.success(f"Saved {csv_path.name} and {report_path.name}.")

    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", csv_bytes, "filtered_youtube_history.csv", "text/csv")
