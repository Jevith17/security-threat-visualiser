import json
from datetime import datetime, timezone

from features.normalizer import normalize_abuseipdb_record
from events.aggregator import aggregate_signals
from scoring.rules import rule_based_ddos_score
from scoring.labels import risk_label

with open("data/raw/abuseipdb_blacklist_sample.json") as f:
    raw = json.load(f)

normalized = [
    normalize_abuseipdb_record(
        record,
        fetched_at=datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    for record in raw["data"]
]

events = aggregate_signals(normalized)

for e in events:
    score = rule_based_ddos_score(e)
    print({
        "source_ip": e.source_ip,
        "score": score,
        "risk": risk_label(score),
        "reports": e.total_reports,
        "confidence": e.max_confidence,
    })
