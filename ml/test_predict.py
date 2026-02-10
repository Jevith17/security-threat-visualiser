import json
from datetime import datetime, timezone

from sklearn.linear_model import LogisticRegression

from features.normalizer import normalize_abuseipdb_record
from events.aggregator import aggregate_signals
from scoring.rules import rule_based_ddos_score
from ml.features import event_to_features


# Load sample data
with open("data/raw/abuseipdb_blacklist_sample.json") as f:
    raw = json.load(f)

# Normalize
normalized = [
    normalize_abuseipdb_record(
        record,
        fetched_at=datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    for record in raw["data"]
]

# Aggregate
events = aggregate_signals(normalized)

# Train model again
X, y = [], []
for e in events:
    X.append(event_to_features(e))
    y.append(1 if rule_based_ddos_score(e) >= 0.75 else 0)

model = LogisticRegression()
model.fit(X, y)

# Predict
for e in events:
    ml_score = model.predict_proba([event_to_features(e)])[0][1]
    rule_score = rule_based_ddos_score(e)

    final_score = 0.5 * rule_score + 0.5 * ml_score

    print({
        "source_ip": e.source_ip,
        "rule_score": round(rule_score, 3),
        "ml_score": round(ml_score, 3),
        "final_score": round(final_score, 3),
    })
