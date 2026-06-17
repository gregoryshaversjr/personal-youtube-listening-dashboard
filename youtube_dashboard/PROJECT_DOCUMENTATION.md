# Personal YouTube Listening Behavior Dashboard Documentation

## Project Overview

The Personal YouTube Listening Behavior Dashboard is a Python-based web application that helps a user explore their YouTube watching, searching, and listening habits. The application uses YouTube Takeout history data, cleans it into a structured format, and displays the results through an interactive Streamlit dashboard.

The project is designed as a school-friendly prototype. It is simple enough to understand and rebuild manually, but complete enough to demonstrate data upload, cleaning, filtering, analysis, visualization, insights, and export features.

## System Architecture

The application uses a modular architecture. Each file has a specific responsibility, and the main Streamlit app connects all modules together.

### Overall Structure

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

### Main Components

| Component | File | Purpose |
| --- | --- | --- |
| User Interface | `app.py` | Runs the dashboard, sidebar, upload controls, tabs, metrics, charts, tables, and export actions. |
| Data Loading | `data_loader.py` | Loads demo data and uploaded YouTube Takeout files. |
| Data Cleaning | `cleaner.py` | Cleans raw records, parses dates, creates helper columns, and filters the dataset. |
| Data Analysis | `analyzer.py` | Calculates totals, trends, top channels, top titles, and activity summaries. |
| Charting | `charts.py` | Builds interactive Altair charts. |
| Insights | `insights.py` | Generates plain-language observations from the filtered data. |
| Report Export | `report_writer.py` | Saves cleaned CSV files and text summary reports. |
| Configuration | `config.py` | Stores shared paths and constants. |

### Architecture Summary

The system is separated into presentation, processing, analysis, visualization, and output layers. This makes the project easier to understand because each part of the code has one main job.

## Data Design

The application stores, retrieves, and manipulates YouTube activity records. The data begins as raw YouTube Takeout history files and is transformed into a clean table for analysis.

### Data Sources

The app can use:

- Built-in demo JSON data
- Uploaded `watch-history.html`
- Uploaded `search-history.html`
- Uploaded cleaned CSV files
- Uploaded cleaned JSON files
- Uploaded ZIP or TGZ Google Takeout archives

### Stored Data

The prototype uses local file storage instead of a database.

| Storage Location | Purpose |
| --- | --- |
| `data/greg_demo_youtube_data.json` | Built-in demo dataset used when the app first opens. |
| `output/cleaned_history.csv` | Exported cleaned dataset. |
| `output/summary_report.txt` | Exported text summary report. |
| Streamlit session state | Temporarily stores the active cleaned dataset while the app is running. |

### Main Data Fields

| Field | Description |
| --- | --- |
| `title` | Video title or search term. |
| `channel` | YouTube channel name or `YouTube Search` for search records. |
| `url` | Link connected to the watched video or search record. |
| `watched_at` | Original timestamp from YouTube Takeout. |
| `content_type` | Type of record, such as `YouTube` or `Search`. |
| `keyword_match` | Searchable text used for keyword filtering. |
| `watch_date` | Clean date value used for filtering and grouping. |
| `watch_time` | Clean time value displayed in the records table. |
| `month` | Month value used for monthly charts. |
| `day_of_week` | Day name used for weekly behavior analysis. |
| `hour` | Hour of day used for hourly activity charts. |

### Data Manipulation

The application manipulates data by:

- Reading uploaded files
- Parsing HTML Takeout records
- Combining multiple uploaded files
- Filling missing values
- Converting timestamps into local time
- Creating helper columns
- Filtering by date range, channel, activity type, and keyword
- Grouping records for charts and metrics
- Exporting filtered data

## User Interface Design

The user interface is built with Streamlit. The design goal is to keep the app simple, clean, and visually polished.

### Visual Style

The dashboard uses a light theme with these colors:

| Color | Hex Code | Usage |
| --- | --- | --- |
| Vibrant Orange | `#FF6B35` | Buttons, highlights, selected tabs, and accent elements. |
| Deep Navy Blue | `#004E64` | Sidebar buttons, chart bars, labels, and major interface accents. |
| Charcoal Gray | `#252525` | Main text. |
| Clean White | `#FFFFFF` | Page background and panels. |

### Main Interface Areas

| Area | Description |
| --- | --- |
| Header | Shows the dashboard title and current dataset name. |
| Sidebar | Contains profile name, upload feature, reset button, and filters. |
| Snapshot Metrics | Shows total records, top channel, most active day, and date range. |
| Tabs | Organizes the app into Overview, Channels & Titles, Records, and Export sections. |
| Charts | Shows interactive visualizations for trends and activity patterns. |
| Insights | Shows short written observations about the filtered data. |
| Records Table | Displays the cleaned activity records. |
| Export Section | Allows the user to save or download filtered results. |

### Wireframe

```text
 ---------------------------------------------------------------
| Personal YouTube Listening Behavior Dashboard                 |
| Current dataset: Greg's Demo YouTube Data                     |
 ---------------------------------------------------------------

 --------------------        -----------------------------------
| Dashboard Controls |      | Snapshot Metrics                  |
|                    |      | Total | Top Channel | Day | Range |
| Profile Name       |       -----------------------------------
| Upload Files       |
| Process Upload     |       -----------------------------------
| Reset Demo Data    |      | Tabs                              |
|                    |      | Overview | Channels | Records | Export |
| Date Range         |       -----------------------------------
| Channel Filter     |
| Activity Type      |       -----------------------------------
| Keyword Search     |      | Charts and Insights               |
 --------------------       | Activity Over Time                |
                             | Activity by Month                |
                             | Activity by Day                  |
                             | Activity by Hour                 |
                             | Written Insights                 |
                              -----------------------------------
```

### Prototype

The working prototype is the Streamlit app:

```text
http://127.0.0.1:8502/
```

The prototype already includes real interaction through file upload, filtering, tabs, charts, tables, and export buttons.

## Module/Component Design

The system is divided into smaller modules so the code is easier to read, test, and rebuild.

### `app.py`

Purpose:

- Runs the Streamlit application.
- Displays the dashboard interface.
- Connects the other modules together.

Main interactions:

- Calls `load_demo_data()` and `load_uploaded_files()` from `data_loader.py`.
- Calls `clean_history()` and `filter_history()` from `cleaner.py`.
- Calls analysis functions from `analyzer.py`.
- Calls chart functions from `charts.py`.
- Calls `generate_insights()` from `insights.py`.
- Calls export functions from `report_writer.py`.

### `data_loader.py`

Purpose:

- Loads data from files into Pandas DataFrames.

Inputs:

- JSON files
- CSV files
- HTML Takeout files
- ZIP archives
- TGZ archives

Outputs:

- Raw Pandas DataFrame records ready for cleaning.

### `cleaner.py`

Purpose:

- Converts raw records into a consistent clean format.

Main functions:

- `clean_history(raw_df)`
- `filter_history(df, keyword, channel, content_type, start_date, end_date)`

Outputs:

- Cleaned and filtered Pandas DataFrames.

### `analyzer.py`

Purpose:

- Performs calculations used by the dashboard.

Main functions:

- `summary_metrics(df)`
- `top_channels(df)`
- `top_titles(df)`
- `activity_by_date(df)`
- `activity_by_month(df)`
- `activity_by_day(df)`
- `activity_by_hour(df)`

Outputs:

- Metrics, Pandas Series, and grouped DataFrames.

### `charts.py`

Purpose:

- Creates interactive charts with Altair.

Main functions:

- `activity_date_chart(df)`
- `vertical_bar_chart(df, x_column, y_column, x_title, y_title, color)`
- `series_bar_chart(series, name_column, count_column)`

Outputs:

- Altair chart objects displayed inside Streamlit.

### `insights.py`

Purpose:

- Converts analysis results into readable observations.

Main function:

- `generate_insights(df)`

Outputs:

- A list of written insight statements.

### `report_writer.py`

Purpose:

- Saves cleaned data and summary reports.

Main functions:

- `save_cleaned_csv(df)`
- `save_summary_report(df)`

Outputs:

- CSV file
- Text report file

### `config.py`

Purpose:

- Stores shared project settings.

Examples:

- Base directory
- Data directory
- Output directory
- Demo dataset path
- Default dataset name

## Testing Strategy

Testing will make sure the app loads data correctly, cleans records properly, filters accurately, displays expected dashboard results, and exports usable files.

### Testing Methods

| Method | Purpose |
| --- | --- |
| Unit Testing | Test individual functions such as cleaning, filtering, and analysis functions. |
| Integration Testing | Test that loading, cleaning, filtering, charting, and exporting work together. |
| Manual UI Testing | Use the Streamlit interface to confirm controls, tabs, charts, and uploads work correctly. |
| Data Validation Testing | Confirm that cleaned data has required columns and correct date formats. |
| Export Testing | Confirm that CSV and text reports are created correctly. |

### Test Cases

| Test Case | Scenario | Expected Outcome |
| --- | --- | --- |
| Load demo data | Open the app without uploading a file. | Demo dataset loads and dashboard metrics appear. |
| Upload HTML history | Upload `watch-history.html` or `search-history.html`. | App formats records and updates the dashboard. |
| Upload archive | Upload a ZIP or TGZ Takeout archive. | App finds history files, parses them, and displays cleaned results. |
| Invalid upload | Upload a file type that is not supported. | App shows an error message and does not crash. |
| Missing values | Load records with missing title, channel, or URL values. | App fills missing values with safe defaults. |
| Date parsing | Load records with valid YouTube timestamps. | App creates `watch_date`, `watch_time`, `month`, `day_of_week`, and `hour`. |
| Date filter | Select a smaller date range. | Metrics, charts, insights, and table update to match the selected range. |
| Channel filter | Select one channel. | Dashboard only shows records from that channel. |
| Activity type filter | Select `YouTube` or `Search`. | Dashboard only shows the selected activity type. |
| Keyword search | Enter a keyword. | Dashboard only shows records where the title or channel matches the keyword. |
| Empty results | Use filters that match no records. | App shows a no-records message instead of crashing. |
| Chart interaction | Hover over bars or points in charts. | Tooltips show readable values. |
| Export CSV | Click the export or download option. | A CSV file is created or downloaded. |
| Export report | Click save summary report. | A text report is created with metrics, top channels, and insights. |

### Manual UI Checklist

- Sidebar appears and can be opened or collapsed.
- Upload button is visible.
- Filters are readable and usable.
- Tabs switch correctly.
- Charts display without overlapping text.
- Export buttons work.
- App uses the intended white, orange, navy, and charcoal color palette.

## Implementation Plan

The project can be completed in milestones. Each milestone produces a clear deliverable.

### Milestone 1: Project Setup

Timeline:

- 1 day

Deliverables:

- Python project folder
- Required libraries installed
- Basic Streamlit app running
- Initial file structure created

### Milestone 2: Data Loading

Timeline:

- 1 to 2 days

Deliverables:

- Demo dataset loading
- Upload support for JSON, CSV, HTML, ZIP, and TGZ files
- Basic error handling for unsupported or empty files

### Milestone 3: Data Cleaning

Timeline:

- 1 to 2 days

Deliverables:

- Cleaned DataFrame structure
- Date parsing
- Missing value handling
- Helper columns such as month, day of week, and hour

### Milestone 4: Analysis Functions

Timeline:

- 1 day

Deliverables:

- Summary metrics
- Top channels
- Top titles
- Activity by date, month, day, and hour

### Milestone 5: Dashboard Interface

Timeline:

- 2 to 3 days

Deliverables:

- Header section
- Sidebar controls
- Metrics section
- Tabs
- Records table
- User-friendly layout

### Milestone 6: Interactive Charts and Insights

Timeline:

- 1 to 2 days

Deliverables:

- Interactive Altair charts
- Hover tooltips
- Written insights section

### Milestone 7: Export Features

Timeline:

- 1 day

Deliverables:

- Save cleaned CSV
- Save text summary report
- Download filtered CSV

### Milestone 8: Styling and Polish

Timeline:

- 1 to 2 days

Deliverables:

- Final color palette
- Clean sidebar
- Readable tabs and buttons
- Polished chart layout
- Consistent visual design

### Milestone 9: Testing and Final Review

Timeline:

- 1 to 2 days

Deliverables:

- Manual UI testing
- Upload testing
- Filter testing
- Export testing
- Final documentation review

## Final Deliverables

The final project should include:

- Working Streamlit dashboard
- Clean modular Python code
- Requirements analysis
- System architecture documentation
- Data design documentation
- User interface design documentation
- Module/component design documentation
- Testing strategy
- Implementation plan
- Demo dataset
- Exportable CSV and text report functionality
