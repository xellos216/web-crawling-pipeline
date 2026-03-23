# src/utils/rate_limit.py

from __future__ import annotations

import logging
import random
import time

from config import RATE_LIMIT_MAX_SECONDS, RATE_LIMIT_MIN_SECONDS


def sleep_between_requests() -> None:
    logger = logging.getLogger(__name__)

    delay = random.uniform(
        RATE_LIMIT_MIN_SECONDS,
        RATE_LIMIT_MAX_SECONDS,
    )
    logger.info("Sleeping for %.2f seconds before next request", delay)
    time.sleep(delay)
