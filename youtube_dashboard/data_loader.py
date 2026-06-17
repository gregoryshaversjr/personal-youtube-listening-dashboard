"""Load YouTube Takeout data from JSON, CSV, or HTML history files."""

from __future__ import annotations

import json
import re
import tarfile
import zipfile
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
from typing import Iterable

import pandas as pd

from config import DEMO_DATA_PATH, DEMO_DATASET_NAME, SAMPLE_DATA_PATH, SAMPLE_DATASET_NAME


DATE_PATTERN = re.compile(
    r"(?P<date>[A-Z][a-z]{2} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2} [AP]M [A-Z]{2,4})$"
)


class TakeoutHistoryParser(HTMLParser):
    """Extract watch and search records from Google Takeout history HTML."""

    def __init__(self, content_type: str):
        super().__init__()
        self.content_type = content_type
        self.records: list[dict[str, str]] = []
        self._in_cell = False
        self._in_link = False
        self._parts: list[str] = []
        self._links: list[tuple[str, str]] = []
        self._link_text = ""
        self._link_href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "div" and "content-cell" in (attrs_dict.get("class") or ""):
            self._in_cell = True
            self._parts = []
            self._links = []
        elif self._in_cell and tag == "a":
            self._in_link = True
            self._link_text = ""
            self._link_href = attrs_dict.get("href") or ""
        elif self._in_cell and tag == "br":
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._in_cell and tag == "a" and self._in_link:
            self._links.append((self._link_text.strip(), self._link_href))
            self._in_link = False
        elif tag == "div" and self._in_cell:
            text = " ".join("".join(self._parts).split())
            record = self._build_record(text)
            if record:
                self.records.append(record)
            self._in_cell = False

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._parts.append(data)
        if self._in_link:
            self._link_text += data

    def _build_record(self, text: str) -> dict[str, str] | None:
        if self.content_type == "Search" and text.startswith("Searched for ") and self._links:
            return self._search_record(text)
        if self.content_type == "YouTube" and text.startswith("Watched ") and self._links:
            return self._watch_record(text)
        return None

    def _search_record(self, text: str) -> dict[str, str] | None:
        match = DATE_PATTERN.search(text)
        if not match:
            return None
        term, url = self._links[0]
        return {
            "title": term,
            "channel": "YouTube Search",
            "url": url,
            "watched_at": match.group("date"),
            "content_type": "Search",
            "keyword_match": term,
        }

    def _watch_record(self, text: str) -> dict[str, str] | None:
        match = DATE_PATTERN.search(text)
        if not match:
            return None
        title, url = self._links[0]
        channel = self._links[1][0] if len(self._links) > 1 else "Unknown Channel"
        return {
            "title": title,
            "channel": channel,
            "url": url,
            "watched_at": match.group("date"),
            "content_type": "YouTube",
            "keyword_match": "",
        }


def load_demo_data() -> pd.DataFrame:
    """Load the saved demo dataset."""
    if DEMO_DATA_PATH.exists():
        return load_json_file(DEMO_DATA_PATH)
    return load_json_file(SAMPLE_DATA_PATH)


def get_demo_dataset_name() -> str:
    """Return the label for the demo dataset available in this environment."""
    if DEMO_DATA_PATH.exists():
        return DEMO_DATASET_NAME
    return SAMPLE_DATASET_NAME


def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    """Load a file uploaded through Streamlit."""
    filename = uploaded_file.name.lower()
    suffix = Path(filename).suffix.lower()
    data = uploaded_file.getvalue()
    if filename.endswith((".tgz", ".tar.gz")):
        return load_takeout_tgz_bytes(data)
    if suffix == ".zip":
        return load_takeout_zip_bytes(data)
    if suffix == ".json":
        return load_json_bytes(data)
    if suffix == ".csv":
        return pd.read_csv(BytesIO(data))
    if suffix in {".html", ".htm"}:
        content_type = "Search" if "search" in uploaded_file.name.lower() else "YouTube"
        return parse_takeout_html(data.decode("utf-8", errors="ignore"), content_type)
    raise ValueError("Please upload a JSON, CSV, YouTube Takeout HTML file, ZIP file, or TGZ file.")


def load_uploaded_files(uploaded_files) -> pd.DataFrame:
    """Load and combine one or more uploaded YouTube data files."""
    frames = [load_uploaded_file(uploaded_file) for uploaded_file in uploaded_files]
    return _combine_uploaded_frames(frames)


def load_json_file(path: Path) -> pd.DataFrame:
    """Load records from a JSON file path."""
    with path.open("r", encoding="utf-8") as file:
        return pd.DataFrame(json.load(file))


def load_json_bytes(data: bytes) -> pd.DataFrame:
    """Load records from uploaded JSON bytes."""
    return pd.DataFrame(json.loads(data.decode("utf-8")))


def parse_takeout_html(html: str, content_type: str) -> pd.DataFrame:
    """Parse a YouTube Takeout HTML history file into a DataFrame."""
    parser = TakeoutHistoryParser(content_type)
    parser.feed(html)
    return pd.DataFrame(parser.records)


def load_takeout_tgz_bytes(data: bytes) -> pd.DataFrame:
    """Load watch/search history from a Google Takeout .tgz or .tar.gz archive."""
    frames = []
    with tarfile.open(fileobj=BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            name = member.name.lower()
            if not member.isfile() or not _is_history_file(name):
                continue
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            content_type = _content_type_from_name(name)
            html = extracted.read().decode("utf-8", errors="ignore")
            frames.append(parse_takeout_html(html, content_type))
    return _combine_uploaded_frames(frames)


def load_takeout_zip_bytes(data: bytes) -> pd.DataFrame:
    """Load watch/search history from a Google Takeout .zip archive."""
    frames = []
    with zipfile.ZipFile(BytesIO(data)) as archive:
        for name in archive.namelist():
            lower_name = name.lower()
            if not _is_history_file(lower_name):
                continue
            content_type = _content_type_from_name(lower_name)
            html = archive.read(name).decode("utf-8", errors="ignore")
            frames.append(parse_takeout_html(html, content_type))
    return _combine_uploaded_frames(frames)


def load_takeout_history_files(paths: Iterable[Path]) -> pd.DataFrame:
    """Load multiple Takeout HTML history files and combine them."""
    frames = []
    for path in paths:
        content_type = "Search" if "search" in path.name.lower() else "YouTube"
        frames.append(parse_takeout_html(path.read_text(encoding="utf-8", errors="ignore"), content_type))
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _is_history_file(name: str) -> bool:
    """Return True for Takeout watch/search history HTML files."""
    return name.endswith(("watch-history.html", "search-history.html"))


def _content_type_from_name(name: str) -> str:
    """Choose dashboard content type from a Takeout filename."""
    return "Search" if "search-history" in name else "YouTube"


def _combine_uploaded_frames(frames: list[pd.DataFrame]) -> pd.DataFrame:
    """Combine uploaded frames or raise a clear upload error."""
    frames = [frame for frame in frames if not frame.empty]
    if not frames:
        raise ValueError("No watch-history.html or search-history.html records were found in this upload.")
    return pd.concat(frames, ignore_index=True)


def dataframe_to_json_records(df: pd.DataFrame) -> str:
    """Convert a DataFrame to pretty JSON records."""
    return df.to_json(orient="records", indent=2)
