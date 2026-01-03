
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict

from events.models import AttackEvent


WINDOW_SIZE = timedelta(minutes=15)


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", ""))


def aggregate_signals(signals: List[Dict]) -> List[AttackEvent]:
    """
    Aggregate normalized threat signals into attack events.
    """

    buckets = defaultdict(list)

    for signal in signals:
        ip = signal["indicator"]["value"]
        fetched_at = parse_iso(signal["fetched_at"])

        window_start = fetched_at - timedelta(
            minutes=fetched_at.minute % 15,
            seconds=fetched_at.second,
            microseconds=fetched_at.microsecond,
        )
        window_end = window_start + WINDOW_SIZE

        key = (ip, window_start)
        buckets[key].append(signal)

    events = []

    for (ip, window_start), grouped_signals in buckets.items():
        event = AttackEvent(
            source_ip=ip,
            window_start=window_start,
            window_end=window_start + WINDOW_SIZE,
            signals=grouped_signals,
        )
        events.append(event)

    return events
