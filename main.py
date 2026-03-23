# main.py

from src.cli.args import parse_args
from src.crawlers.site_a_requests import crawl_site_a
from src.monitoring.logger import setup_logger
from src.storage.json_writer import (
    save_invalid_records,
    save_raw_records,
    save_transformed_records,
    save_valid_records,
)
from src.transformers.listing_transformer import transform_listings
from src.validators.listing_validator import validate_listings
from datetime import datetime
from src.monitoring.run_summary import (
    build_run_summary,
    save_run_summary,
)

from src.crawlers.site_b_playwright import crawl_site_b


def main():
    args = parse_args()
    logger = setup_logger(args.log_level)

    started_at = datetime.now()

    logger.info("=== Web Crawling Pipeline Start ===")
    logger.info("source: %s", args.source)
    logger.info("max_pages: %s", args.max_pages)
    logger.info("limit: %s", args.limit)
    logger.info("use_browser: %s", args.use_browser)
    logger.info("log_level: %s", args.log_level)

    if args.source == "site_a":
        raw_records = crawl_site_a(
            max_pages=args.max_pages,
            limit=args.limit,
        )
    elif args.source == "site_b":
        raw_records = crawl_site_b(
            max_pages=args.max_pages,
            limit=args.limit,
        )
    else:
        raise ValueError(f"Unsupported source: {args.source}")

    raw_path = save_raw_records(raw_records, args.source)

    validation_result = validate_listings(raw_records)
    valid_records = validation_result["valid_records"]
    invalid_records = validation_result["invalid_records"]

    valid_path = save_valid_records(valid_records, args.source)
    invalid_path = save_invalid_records(invalid_records, args.source)

    transformed_records = transform_listings(valid_records)
    transformed_path = save_transformed_records(
        transformed_records,
        args.source,
    )

    logger.info("Raw records saved: %s", raw_path)
    logger.info("Valid records saved: %s", valid_path)
    logger.info("Invalid records saved: %s", invalid_path)
    logger.info("Transformed records saved: %s", transformed_path)

    logger.info("Raw record count: %s", len(raw_records))
    logger.info("Valid record count: %s", len(valid_records))
    logger.info("Invalid record count: %s", len(invalid_records))
    logger.info("Transformed record count: %s", len(transformed_records))

    finished_at = datetime.now()

    summary = build_run_summary(
        source=args.source,
        raw_count=len(raw_records),
        valid_count=len(valid_records),
        invalid_count=len(invalid_records),
        transformed_count=len(transformed_records),
        raw_path=raw_path,
        valid_path=valid_path,
        invalid_path=invalid_path,
        transformed_path=transformed_path,
        started_at=started_at,
        finished_at=finished_at,
    )

    summary_path = save_run_summary(summary)

    logger.info("Run summary saved: %s", summary_path)
    logger.info("=== Pipeline Finished ===")


if __name__ == "__main__":
    main()
