
import time
import logging
import requests

from config.settings import (
    POLL_INTERVAL_SECONDS,
    ABUSEIPDB_API_KEY,
    TOP_N,
)


ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/blacklist"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def fetch_blacklist():
    """
    Fetch top abusive IPs from AbuseIPDB.
    Returns raw JSON response.
    """
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json",
    }

    params = {
        "confidenceMinimum": 1,
        "limit": TOP_N,
    }

    response = requests.get(
        ABUSEIPDB_URL,
        headers=headers,
        params=params,
        timeout=10,
    )

    response.raise_for_status()
    return response.json()
    


def run_worker():
    setup_logging()
    logging.info("AbuseIPDB ingestion worker started")

    while True:
        try:
            logging.info("Fetching top %s abusive IPs", TOP_N)
            data = fetch_blacklist()

            # TEMP: just inspect the data
            logging.info(
                "Fetched %s records from AbuseIPDB",
                len(data.get("data", []))
            )

        except Exception as e:
            logging.error("Ingestion failed: %s", e)

        logging.info("Sleeping for %s seconds", POLL_INTERVAL_SECONDS)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_worker()
