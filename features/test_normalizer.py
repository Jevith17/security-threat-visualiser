import json
from datetime import datetime
from features.normalizer import normalize_abuseipdb_record

with open("data/raw/abuseipdb_blacklist_sample.json") as f:
    raw = json.load(f)

record = raw["data"][0]

normalized = normalize_abuseipdb_record(
    record,
    fetched_at=datetime.utcnow().isoformat() + "Z"
)

print(json.dumps(normalized, indent=2))
