# src/monitoring/logger.py

import logging
import os
from config import LOG_DIR, LOG_FILE, ERROR_LOG_FILE


def setup_logger(log_level: str):
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 기존 핸들러 제거 (중복 방지)
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # 일반 로그
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE))
    file_handler.setFormatter(formatter)

    # 에러 로그
    error_handler = logging.FileHandler(os.path.join(LOG_DIR, ERROR_LOG_FILE))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # 콘솔 출력
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger
