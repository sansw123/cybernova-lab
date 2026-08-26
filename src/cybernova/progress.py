"""A tiny local learning log for portfolio consistency."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path


DEFAULT_PROGRESS_FILE = Path(".cybernova-progress.json")


def load_progress(path: str | Path = DEFAULT_PROGRESS_FILE) -> dict:
    progress_path = Path(path)
    if not progress_path.exists():
        return {"topics": []}
    data = json.loads(progress_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("topics"), list):
        raise ValueError("Invalid progress file")
    return data


def add_topic(topic: str, path: str | Path = DEFAULT_PROGRESS_FILE) -> dict:
    """Record a studied topic in a local JSON file."""

    clean_topic = " ".join(topic.strip().split())
    if not clean_topic:
        raise ValueError("Topic cannot be empty")
    progress_path = Path(path)
    data = load_progress(progress_path)
    data["topics"].append({"topic": clean_topic, "date": date.today().isoformat()})
    progress_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data["topics"][-1]

