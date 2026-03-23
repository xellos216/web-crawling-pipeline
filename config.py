# config.py

LOG_DIR = "logs"
LOG_FILE = "crawler.log"
ERROR_LOG_FILE = "error.log"

DEFAULT_LOG_LEVEL = "INFO"

SITE_A_BASE_URL = "https://books.toscrape.com/catalogue/"
SITE_A_START_URL = "https://books.toscrape.com/catalogue/page-1.html"

SITE_B_START_URL = "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops"

PLAYWRIGHT_HEADLESS = True
PLAYWRIGHT_TIMEOUT_MS = 15000

RAW_DATA_DIR = "data/raw"
VALIDATED_DATA_DIR = "data/validated"
TRANSFORMED_DATA_DIR = "data/transformed"

REQUEST_TIMEOUT = 10
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2.0

RATE_LIMIT_MIN_SECONDS = 1.0
RATE_LIMIT_MAX_SECONDS = 2.5

USER_AGENTS = [
    ("Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0"),
    (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/134.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/134.0.0.0 Safari/537.36"
    ),
]
