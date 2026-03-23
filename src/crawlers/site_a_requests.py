# src/crawlers/site_a_requests.py

from __future__ import annotations

import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import SITE_A_BASE_URL


def crawl_site_a(max_pages: int, limit: int) -> list[dict]:
    logger = logging.getLogger(__name__)
    records: list[dict] = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0"
        )
    }

    for page_num in range(1, max_pages + 1):
        if len(records) >= limit:
            break

        page_url = f"{SITE_A_BASE_URL}page-{page_num}.html"
        logger.info("Fetching page: %s", page_url)

        response = requests.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.product_pod")

        if not articles:
            logger.info("No articles found on page %s", page_num)
            break

        for article in articles:
            if len(records) >= limit:
                break

            title_tag = article.select_one("h3 a")
            price_tag = article.select_one(".price_color")
            availability_tag = article.select_one(".availability")

            if title_tag is None or price_tag is None or availability_tag is None:
                logger.warning("Skipping incomplete article on page %s", page_num)
                continue

            relative_url = title_tag.get("href", "")
            detail_url = urljoin(SITE_A_BASE_URL, relative_url)

            record = {
                "source": "site_a",
                "listing_url": detail_url,
                "title": title_tag.get("title", "").strip(),
                "price_text": price_tag.get_text(strip=True),
                "status_text": availability_tag.get_text(strip=True),
            }
            records.append(record)

        logger.info(
            "Page %s processed. Current record count: %s",
            page_num,
            len(records),
        )

    logger.info("Crawling finished. Total raw records: %s", len(records))
    return records
