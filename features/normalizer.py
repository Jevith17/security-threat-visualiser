
from datetime import datetime


def normalize_abuseipdb_record(record: dict, fetched_at: str) -> dict:
    """
    Convert a single AbuseIPDB IP record into a normalized threat signal.
    """

    return {
        "source": "abuseipdb",
        "indicator": {
            "type": "ip",
            "value": record.get("ipAddress"),
        },
        "signals": {
            "confidence_score": record.get("abuseConfidenceScore"),
            "total_reports": record.get("totalReports"),
            "distinct_reporters": record.get("numDistinctUsers"),
            "last_reported_at": _normalize_timestamp(
                record.get("lastReportedAt")
            ),
        },
        "context": {
            "country": record.get("countryCode"),
            "network_type": record.get("usageType"),
            "isp": record.get("isp"),
        },
        "fetched_at": fetched_at,
    }


def _normalize_timestamp(ts: str | None) -> str | None:
    """
    Normalize timestamps to UTC ISO-8601 without timezone offset.
    """
    if not ts:
        return None

    return (
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
        .astimezone()
        .replace(tzinfo=None)
        .isoformat() + "Z"
    )
