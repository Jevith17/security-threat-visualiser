
import json
from datetime import datetime, timezone

from features.normalizer import normalize_abuseipdb_record
from events.aggregator import aggregate_signals
from scoring.rules import rule_based_ddos_score
from scoring.labels import risk_label
from ml.features import event_to_features
from sklearn.linear_model import LogisticRegression
from geo.resolver import ip_to_geo



class BackendState:
    
    def __init__(self):
        self.events = []
        self.model = None

    def load(self):
        # Load raw data
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

        # Train ML model
        X, y = [], []
        for e in events:
            X.append(event_to_features(e))
            y.append(1 if rule_based_ddos_score(e) >= 0.75 else 0)

        model = LogisticRegression()
        model.fit(X, y)

        # Attach scores
        enriched = []
        for e in events:
            geo = ip_to_geo(e.source_ip)
            if not geo:
                continue

            rule_score = rule_based_ddos_score(e)
            ml_score = model.predict_proba(
                [event_to_features(e)]
            )[0][1]

            final_score = 0.5 * rule_score + 0.5 * ml_score

            enriched.append({
                **e.to_dict(),
                "geo": geo,
                "rule_score": round(rule_score, 3),
                "ml_score": round(ml_score, 3),
                "final_score": round(final_score, 3),
                "risk": risk_label(final_score),
            })

        self.events = enriched
        self.model = model
