# src/cli/args.py

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Web Crawling Pipeline")

    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Data source (e.g., site_a, site_b)",
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="Number of pages to crawl",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Max number of items to collect",
    )

    parser.add_argument(
        "--use-browser",
        action="store_true",
        help="Use browser (Playwright)",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Log level (DEBUG, INFO, ERROR)",
    )

    return parser.parse_args()
