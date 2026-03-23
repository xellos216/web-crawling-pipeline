# src/storage/json_writer.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from config import RAW_DATA_DIR, VALIDATED_DATA_DIR, TRANSFORMED_DATA_DIR


def _build_output_path(base_dir: str, source: str, suffix: str) -> Path:
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(base_dir) / f"{source}_{suffix}_{timestamp}.json"


def save_raw_records(records: list[dict], source: str) -> str:
    file_path = _build_output_path(RAW_DATA_DIR, source, "raw")

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return str(file_path)


def save_valid_records(records: list[dict], source: str) -> str:
    file_path = _build_output_path(VALIDATED_DATA_DIR, source, "valid")

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return str(file_path)


def save_invalid_records(records: list[dict], source: str) -> str:
    file_path = _build_output_path(VALIDATED_DATA_DIR, source, "invalid")

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return str(file_path)


def save_transformed_records(records: list[dict], source: str) -> str:
    file_path = _build_output_path(TRANSFORMED_DATA_DIR, source, "normalized")

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return str(file_path)
