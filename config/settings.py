from os import getenv


def _get_int_setting(name: str, default: int) -> int:
    value = getenv(name)
    if value is None:
        return default
    return int(value)


POLL_INTERVAL_SECONDS = _get_int_setting("POLL_INTERVAL_SECONDS", 300)  # 5 minutes
TOP_N = _get_int_setting("TOP_N", 100)
OUTPUT_DIR = getenv("OUTPUT_DIR", "data/raw")
ABUSEIPDB_API_KEY = getenv("ABUSEIPDB_API_KEY", "")
