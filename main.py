# main.py

from src.cli.args import parse_args
from src.crawlers.site_a_requests import crawl_site_a
from src.monitoring.logger import setup_logger
from src.storage.json_writer import save_raw_records


def main():
    args = parse_args()
    logger = setup_logger(args.log_level)

    logger.info("=== Web Crawling Pipeline Start ===")
    logger.info("source: %s", args.source)
    logger.info("max_pages: %s", args.max_pages)
    logger.info("limit: %s", args.limit)
    logger.info("use_browser: %s", args.use_browser)
    logger.info("log_level: %s", args.log_level)

    if args.source != "site_a":
        raise ValueError(f"Unsupported source: {args.source}")

    raw_records = crawl_site_a(
        max_pages=args.max_pages,
        limit=args.limit,
    )

    raw_path = save_raw_records(raw_records, args.source)

    logger.info("Raw records saved: %s", raw_path)
    logger.info("Raw record count: %s", len(raw_records))
    logger.info("=== Pipeline Finished ===")


if __name__ == "__main__":
    main()
