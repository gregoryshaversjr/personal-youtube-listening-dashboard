# System Architecture

## Overall Structure

The Personal YouTube Listening Behavior Dashboard is organized as a small modular Python application. The main program is a Streamlit web app, and the supporting modules handle data loading, cleaning, analysis, chart creation, insights, and export.

The architecture follows a simple pipeline:

```text
YouTube Takeout Data
        |
        v
Data Loader
        |
        v
Data Cleaner
        |
        v
Analyzer + Insights
        |
        v
Charts + Tables + Metrics
        |
        v
Streamlit Dashboard
        |
        v
CSV / Text Report Export
```

## Main Components

| Component | File | Responsibility |
| --- | --- | --- |
| User Interface | `app.py` | Runs the Streamlit dashboard, sidebar controls, upload form, tabs, metrics, charts, tables, and export buttons. |
| Data Loading | `data_loader.py` | Loads demo data and uploaded YouTube Takeout files, including JSON, CSV, HTML, ZIP, TGZ, and GZ files. |
| Data Cleaning | `cleaner.py` | Standardizes raw records, parses dates, fills missing values, creates helper columns, and applies dashboard filters. |
| Data Analysis | `analyzer.py` | Calculates totals, top channels, top titles, activity by date, activity by month, activity by day, and activity by hour. |
| Charting | `charts.py` | Builds interactive Altair charts used in the dashboard. |
| Insight Generation | `insights.py` | Creates short written observations based on the filtered data. |
| Exporting | `report_writer.py` | Saves cleaned CSV files and plain text summary reports. |
| Configuration | `config.py` | Stores shared paths and constants such as the demo dataset path and output folder. |

## Data Flow

1. The app starts in `app.py`.
2. Streamlit loads the built-in demo dataset from `data/greg_demo_youtube_data.json`.
3. If the user uploads their own YouTube data, `data_loader.py` reads the uploaded file or archive.
4. `cleaner.py` formats the raw data into a consistent table.
5. Sidebar filters in `app.py` send the cleaned data back through `filter_history()`.
6. `analyzer.py` calculates metrics and grouped activity summaries.
7. `charts.py` turns the analysis results into interactive visualizations.
8. `insights.py` generates short explanations of the user’s behavior patterns.
9. `report_writer.py` can export the filtered results as a CSV file and summary report.

## Program Layers

### Presentation Layer

The presentation layer is handled by `app.py` using Streamlit. This layer is responsible for everything the user sees and clicks:

- Page title and dashboard header
- Sidebar controls
- File upload section
- Date, channel, activity type, and keyword filters
- Snapshot metrics
- Dashboard tabs
- Charts and tables
- Export buttons
- Custom visual styling

### Data Processing Layer

The data processing layer is handled by `data_loader.py` and `cleaner.py`.

`data_loader.py` converts external files into Pandas DataFrames. It supports multiple input types so the user can upload different versions of YouTube Takeout data.

`cleaner.py` prepares the data for analysis. It makes sure required columns exist, cleans text values, parses dates, converts timestamps to local time, and creates helper fields such as month, day of week, hour, and watch date.

### Analysis Layer

The analysis layer is handled by `analyzer.py` and `insights.py`.

`analyzer.py` performs numeric and grouped calculations. It answers questions such as:

- How many total records are in the dataset?
- What channel appears most often?
- Which day is most active?
- How much activity happened each month?
- What hours are busiest?

`insights.py` turns some of those calculations into readable statements for the user.

### Visualization Layer

The visualization layer is handled by `charts.py`. It uses Altair to create interactive charts with hover tooltips and visual highlighting.

The dashboard currently includes:

- Activity over time line chart
- Activity by month bar chart
- Activity by day horizontal bar chart
- Activity by hour bar chart
- Top channels chart

### Output Layer

The output layer is handled by `report_writer.py`. It allows the user to save:

- A cleaned CSV file
- A plain text summary report
- A downloadable filtered CSV from the Streamlit interface

## State Management

The app uses Streamlit session state to remember the current dataset during the user’s session.

Important session values include:

- `clean_df`: the current cleaned DataFrame
- `dataset_name`: the label shown in the dashboard header
- `profile_name`: the temporary name entered in the sidebar
- `upload_summary`: a message describing the uploaded and cleaned data

This means the app can switch between the demo data and uploaded data without needing a database.

## Storage Design

The current prototype uses simple local file storage.

| Storage Area | Purpose |
| --- | --- |
| `data/` | Stores the built-in demo JSON dataset. |
| `output/` | Stores exported CSV files and text reports. |
| Streamlit session state | Temporarily stores the active cleaned dataset while the app is running. |

The prototype does not use a database. This keeps the project easier to understand and rebuild from scratch.

## Architecture Summary

The system uses a simple modular design:

- `app.py` controls the user experience.
- `data_loader.py` brings raw YouTube data into the program.
- `cleaner.py` formats the raw data.
- `analyzer.py` calculates useful patterns.
- `charts.py` displays those patterns visually.
- `insights.py` explains the patterns in plain language.
- `report_writer.py` exports the results.

This structure keeps the app organized while still being simple enough for a school prototype and manual rebuild.
