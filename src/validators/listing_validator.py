# src/validators/listing_validator.py

from __future__ import annotations


def validate_listings(records: list[dict]) -> dict[str, list[dict]]:
    valid_records: list[dict] = []
    invalid_records: list[dict] = []

    for record in records:
        errors: list[str] = []

        source = str(record.get("source", "")).strip()
        listing_url = str(record.get("listing_url", "")).strip()
        title = str(record.get("title", "")).strip()
        price_text = str(record.get("price_text", "")).strip()

        if not source:
            errors.append("missing_source")

        if not listing_url:
            errors.append("missing_listing_url")
        elif not (
            listing_url.startswith("http://") or listing_url.startswith("https://")
        ):
            errors.append("invalid_listing_url")

        if not title:
            errors.append("missing_title")

        if not price_text:
            errors.append("missing_price_text")

        if errors:
            invalid_record = record.copy()
            invalid_record["validation_errors"] = errors
            invalid_records.append(invalid_record)
        else:
            valid_records.append(record)

    return {
        "valid_records": valid_records,
        "invalid_records": invalid_records,
    }
