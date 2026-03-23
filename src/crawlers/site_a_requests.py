# src/crawlers/site_a_requests.py

from __future__ import annotations

import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT, SITE_A_BASE_URL
from src.utils.rate_limit import sleep_between_requests
from src.utils.retry import request_with_retry
from src.utils.user_agent import get_random_user_agent


def crawl_site_a(max_pages: int, limit: int) -> list[dict]:
    logger = logging.getLogger(__name__)
    records: list[dict] = []

    user_agent = get_random_user_agent()
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    }

    logger.info("Selected User-Agent: %s", user_agent)

    for page_num in range(1, max_pages + 1):
        if len(records) >= limit:
            break

        page_url = f"{SITE_A_BASE_URL}page-{page_num}.html"
        logger.info("Fetching page: %s", page_url)

        def do_request() -> requests.Response:
            return requests.get(
                page_url,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )

        response = request_with_retry(do_request, page_url)
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
                logger.warning(
                    "Skipping incomplete article on page %s",
                    page_num,
                )
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

        if len(records) < limit and page_num < max_pages:
            sleep_between_requests()

    logger.info("Crawling finished. Total raw records: %s", len(records))
    return records
