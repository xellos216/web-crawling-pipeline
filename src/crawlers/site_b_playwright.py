# src/crawlers/site_b_playwright.py

from __future__ import annotations

import logging
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from config import (
    PLAYWRIGHT_HEADLESS,
    PLAYWRIGHT_TIMEOUT_MS,
    SITE_B_START_URL,
)
from src.utils.rate_limit import sleep_between_requests
from src.utils.user_agent import get_random_user_agent


def crawl_site_b(max_pages: int, limit: int) -> list[dict]:
    logger = logging.getLogger(__name__)
    records: list[dict] = []

    user_agent = get_random_user_agent()
    logger.info("Selected User-Agent: %s", user_agent)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=PLAYWRIGHT_HEADLESS)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        logger.info("Opening dynamic page: %s", SITE_B_START_URL)
        page.goto(SITE_B_START_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)

        for page_num in range(1, max_pages + 1):
            if len(records) >= limit:
                break

            logger.info("Processing dynamic page number: %s", page_num)

            page.wait_for_selector(".product-wrapper", timeout=PLAYWRIGHT_TIMEOUT_MS)

            items = page.locator(".product-wrapper")
            item_count = items.count()

            if item_count == 0:
                logger.info("No items found on dynamic page %s", page_num)
                break

            for i in range(item_count):
                if len(records) >= limit:
                    break

                item = items.nth(i)

                title_el = item.locator(".title")
                price_el = item.locator(".price")
                link_el = item.locator(".title")

                title = title_el.inner_text().strip()
                price_text = price_el.inner_text().strip()
                relative_url = link_el.get_attribute("href") or ""
                detail_url = urljoin(SITE_B_START_URL, relative_url)

                record = {
                    "source": "site_b",
                    "listing_url": detail_url,
                    "title": title,
                    "price_text": price_text,
                    "status_text": "unknown",
                }
                records.append(record)

            logger.info(
                "Dynamic page %s processed. Current record count: %s",
                page_num,
                len(records),
            )

            if len(records) >= limit:
                break

            next_button = page.locator("a[rel='next']")
            if next_button.count() == 0 or "disabled" in (
                next_button.get_attribute("class") or ""
            ):
                logger.info("No next page available for site_b")
                break

            sleep_between_requests()
            next_button.click()
            page.wait_for_timeout(1500)

        context.close()
        browser.close()

    logger.info("Dynamic crawling finished. Total raw records: %s", len(records))
    return records
