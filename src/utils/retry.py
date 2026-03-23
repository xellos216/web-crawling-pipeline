# src/utils/retry.py

from __future__ import annotations

import logging
import time
from collections.abc import Callable

import requests

from config import MAX_RETRY_ATTEMPTS, RETRY_DELAY_SECONDS


def request_with_retry(
    request_func: Callable[[], requests.Response],
    url: str,
) -> requests.Response:
    logger = logging.getLogger(__name__)

    last_exception: Exception | None = None

    for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
        try:
            response = request_func()

            if response.status_code >= 500:
                raise requests.HTTPError(
                    f"Server error {response.status_code} for {url}"
                )

            return response

        except (
            requests.Timeout,
            requests.ConnectionError,
            requests.HTTPError,
        ) as exc:
            last_exception = exc
            logger.warning(
                "Request failed (attempt %s/%s) for %s: %s",
                attempt,
                MAX_RETRY_ATTEMPTS,
                url,
                exc,
            )

            if attempt < MAX_RETRY_ATTEMPTS:
                logger.info(
                    "Retrying in %.1f seconds: %s",
                    RETRY_DELAY_SECONDS,
                    url,
                )
                time.sleep(RETRY_DELAY_SECONDS)

    assert last_exception is not None
    raise last_exception
