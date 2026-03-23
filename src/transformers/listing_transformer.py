# src/transformers/listing_transformer.py

from __future__ import annotations

from datetime import datetime
from urllib.parse import urlparse


def extract_item_id(detail_url: str) -> str:
    path = urlparse(detail_url).path.strip("/")
    parts = path.split("/")

    if len(parts) >= 2:
        return parts[-2]

    return ""


def parse_price(price_text: str) -> float:
    cleaned = "".join(ch for ch in price_text if ch.isdigit() or ch == ".")
    return float(cleaned)


def normalize_status(status_text: str) -> str:
    cleaned = " ".join(status_text.split()).lower()

    if "in stock" in cleaned:
        return "in_stock"

    return "unknown"


def transform_listings(records: list[dict]) -> list[dict]:
    transformed_records: list[dict] = []

    for record in records:
        detail_url = str(record.get("listing_url", "")).strip()
        title = str(record.get("title", "")).strip()
        price_text = str(record.get("price_text", "")).strip()
        status_text = str(record.get("status_text", "")).strip()
        source = str(record.get("source", "")).strip()

        transformed_record = {
            "source": source,
            "item_id": extract_item_id(detail_url),
            "title": title,
            "price": parse_price(price_text),
            "currency": "GBP",
            "status": normalize_status(status_text),
            "detail_url": detail_url,
            "collected_at": datetime.now().isoformat(timespec="seconds"),
        }

        transformed_records.append(transformed_record)

    return transformed_records
