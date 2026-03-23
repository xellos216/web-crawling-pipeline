# src/monitoring/run_summary.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


REPORTS_DIR = "reports"
SUMMARY_FILE = "latest_run_summary.json"


def build_run_summary(
    source: str,
    raw_count: int,
    valid_count: int,
    invalid_count: int,
    transformed_count: int,
    raw_path: str,
    valid_path: str,
    invalid_path: str,
    transformed_path: str,
    started_at: datetime,
    finished_at: datetime,
) -> dict:
    return {
        "source": source,
        "started_at": started_at.isoformat(timespec="seconds"),
        "finished_at": finished_at.isoformat(timespec="seconds"),
        "duration_seconds": (finished_at - started_at).total_seconds(),
        "counts": {
            "raw": raw_count,
            "valid": valid_count,
            "invalid": invalid_count,
            "transformed": transformed_count,
        },
        "paths": {
            "raw": raw_path,
            "valid": valid_path,
            "invalid": invalid_path,
            "transformed": transformed_path,
        },
    }


def save_run_summary(summary: dict) -> str:
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)

    file_path = Path(REPORTS_DIR) / SUMMARY_FILE

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return str(file_path)
