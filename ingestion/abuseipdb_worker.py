
import json
import logging
from datetime import datetime
from pathlib import Path

import requests

from config.settings import ABUSEIPDB_API_KEY, OUTPUT_DIR, TOP_N


ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/blacklist"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def fetch_blacklist():
    if not ABUSEIPDB_API_KEY:
        raise RuntimeError(
            "ABUSEIPDB_API_KEY is required. Set it in your environment before running ingestion."
        )

    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json",
    }

    params = {
        "confidenceMinimum": 25,
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


def save_raw_response(data: dict):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"abuseipdb_blacklist_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    logging.info("Saved raw blacklist data to %s", file_path)


def main():
    setup_logging()
    logging.info("Fetching AbuseIPDB blacklist (one-time fetch)")

    data = fetch_blacklist()
    save_raw_response(data)

    logging.info("Ingestion complete. Exiting.")


if __name__ == "__main__":
    main()
