import json
from datetime import datetime, timezone

from sklearn.linear_model import LogisticRegression

from features.normalizer import normalize_abuseipdb_record
from events.aggregator import aggregate_signals
from scoring.rules import rule_based_ddos_score
from ml.features import event_to_features


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

X = []
y = []

for event in events:
    features = event_to_features(event)
    label = 1 if rule_based_ddos_score(event) >= 0.75 else 0

    X.append(features)
    y.append(label)

model = LogisticRegression()
model.fit(X, y)

print("Model coefficients:", model.coef_)
print("Intercept:", model.intercept_)
