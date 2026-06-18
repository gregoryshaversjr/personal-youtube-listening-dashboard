# Personal YouTube Listening Behavior Dashboard

A Python and Streamlit web app for exploring personal YouTube watching, searching, and listening behavior from Google Takeout history data.

This project was built as a school prototype. The goal is to keep the code simple enough to understand and rebuild by hand, while still showing a real data workflow: upload, clean, filter, analyze, visualize, and export.

## What The App Does

- Loads YouTube Takeout history data from JSON, CSV, HTML, ZIP, or TGZ files.
- Cleans raw YouTube activity records into a structured table.
- Filters activity by date range, channel, activity type, and keyword.
- Displays dashboard metrics such as total records, top channel, most active day, and date range.
- Shows interactive charts for activity over time, month, day, and hour.
- Generates short written insights from the filtered data.
- Exports cleaned data and summary reports.

## Project Structure

```text
youtube_dashboard/
├── app.py
├── data_loader.py
├── cleaner.py
├── analyzer.py
├── charts.py
├── insights.py
├── report_writer.py
├── config.py
├── requirements.txt
├── data/
└── scripts/
```

## Libraries Used

- `streamlit` for the web app interface
- `pandas` for data cleaning, filtering, and analysis
- `altair` for interactive charts

## How To Run The App

```bash
cd youtube_dashboard
pip install -r requirements.txt
streamlit run app.py
```

After the command runs, open:

```text
http://127.0.0.1:8502
```

## Data Privacy

The real personal YouTube history file is intentionally excluded from GitHub with `.gitignore`. The repository includes a small sample dataset so the app can still run without exposing private data.

## Documentation

The project includes supporting school documentation inside the `youtube_dashboard` folder:

- `PROJECT_DOCUMENTATION.md`
- `REQUIREMENTS_ANALYSIS.md`
- `SYSTEM_ARCHITECTURE.md`

## Status

This is a working local prototype. It is not deployed as a public website yet.
