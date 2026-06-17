# Requirements Analysis

## Necessary Libraries

This application is a Python-based dashboard that cleans and displays personal YouTube Takeout history data. The required libraries are intentionally simple so the project stays beginner-friendly and easy to rebuild manually.

### Python Standard Library

The project uses several built-in Python libraries. These do not need to be installed separately.

- `json`: Reads saved dashboard data from JSON files.
- `re`: Searches raw Takeout text using regular expressions.
- `tarfile`: Opens Google Takeout `.tgz` and `.tar.gz` archive uploads.
- `zipfile`: Opens Google Takeout `.zip` archive uploads.
- `html.parser`: Parses YouTube Takeout HTML history files.
- `io.BytesIO`: Reads uploaded files from memory.
- `pathlib`: Handles file and folder paths.
- `typing`: Adds clearer type hints for iterable inputs.
- `html.escape`: Safely displays text inside custom HTML blocks.

### External Libraries

These libraries must be installed before running the app.

| Library | Purpose |
| --- | --- |
| `streamlit` | Builds the web dashboard interface, sidebar controls, file uploader, tabs, metrics, tables, and page layout. |
| `pandas` | Cleans, filters, groups, and analyzes the YouTube history data. |
| `altair` | Creates interactive charts for activity over time, activity by day, activity by hour, monthly activity, top channels, and top titles. |

## Why These Libraries Are Needed

`Streamlit` is used because it allows a Python application to become an interactive web dashboard without needing a separate frontend framework. It is responsible for the visible app, including the upload feature, sidebar filters, buttons, tabs, and dashboard sections.

`Pandas` is used because the raw YouTube Takeout files need to be turned into structured data. Pandas helps clean date values, separate columns, remove missing records, filter by date or keyword, and calculate summary statistics.

`Altair` is used because the app needs interactive graphs. It works well with Pandas DataFrames and allows charts to support hover tooltips, zooming, and cleaner visual styling.

The Python standard library is used for file handling and data parsing. This keeps the project lightweight because archive support, HTML parsing, JSON reading, and path handling can be done without adding many extra dependencies.

## Installation Requirements

The current `requirements.txt` file should contain:

```txt
pandas
streamlit
altair
```

To install the required libraries, run:

```bash
pip install -r requirements.txt
```

## Requirement Summary

The app only needs three external libraries: `streamlit`, `pandas`, and `altair`. This keeps the application simple, readable, and realistic for a school prototype while still supporting data upload, cleaning, analysis, and interactive visualizations.
