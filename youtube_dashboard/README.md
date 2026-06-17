# Personal YouTube Listening Behavior Dashboard

This is a beginner-friendly Python prototype for a school project. It loads YouTube Takeout history data, cleans it with Pandas, and displays an interactive dashboard with Streamlit.

## Project Structure

- `app.py` runs the Streamlit dashboard.
- `data_loader.py` loads JSON, CSV, and YouTube Takeout HTML history files.
- `cleaner.py` cleans dates, titles, channels, and helper columns.
- `analyzer.py` calculates totals, top channels, top titles, and trends.
- `insights.py` writes simple observations from the data.
- `report_writer.py` exports cleaned CSV files and text reports.
- `config.py` stores project paths and constants.

## Run the Prototype

```bash
cd youtube_dashboard
pip install -r requirements.txt
streamlit run app.py
```

The app opens with local demo data when available. Personal demo data is intentionally ignored by Git so private YouTube history is not published. If that private file is missing, the app falls back to `data/sample_youtube_data.json`.

You can also upload a YouTube Takeout `watch-history.html`, `search-history.html`, CSV, JSON, ZIP, or TGZ file during the session.

## Learning Path

1. Start with `app.py` to see how the user interface calls the other modules.
2. Open `data_loader.py` to understand how raw Takeout HTML becomes rows.
3. Open `cleaner.py` to see how messy text turns into useful date columns.
4. Open `analyzer.py` and `insights.py` to learn how charts and written observations are calculated.
5. Rebuild one module at a time by hand after you understand its job.
