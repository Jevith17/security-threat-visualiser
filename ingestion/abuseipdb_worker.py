
import time
import logging

from config.settings import POLL_INTERVAL_SECONDS


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def run_worker():
    setup_logging()
    logging.info("AbuseIPDB ingestion worker started")

    while True:
        logging.info("Worker sleeping for %s seconds", POLL_INTERVAL_SECONDS)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_worker()
