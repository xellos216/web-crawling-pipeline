# src/storage/json_writer.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from config import RAW_DATA_DIR


def save_raw_records(records: list[dict], source: str) -> str:
    Path(RAW_DATA_DIR).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = Path(RAW_DATA_DIR) / f"{source}_{timestamp}.json"

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return str(file_path)
