
from datetime import datetime
from typing import List, Dict


class AttackEvent:
    """
    Represents a time-bounded aggregation of malicious activity
    from a single source IP.
    """

    def __init__(
        self,
        source_ip: str,
        window_start: datetime,
        window_end: datetime,
        signals: List[Dict],
    ):
        self.source_ip = source_ip
        self.window_start = window_start
        self.window_end = window_end
        self.signals = signals

        # Derived attributes (computed later)
        self.total_reports = self._compute_total_reports()
        self.max_confidence = self._compute_max_confidence()
        self.signal_count = len(signals)

    def _compute_total_reports(self) -> int:
        return sum(
            s["signals"].get("total_reports", 0)
            for s in self.signals
        )

    def _compute_max_confidence(self) -> int:
        return max(
            s["signals"].get("confidence_score", 0)
            for s in self.signals
        )

    def to_dict(self) -> Dict:
        return {
            "source_ip": self.source_ip,
            "window_start": self.window_start.isoformat() + "Z",
            "window_end": self.window_end.isoformat() + "Z",
            "signal_count": self.signal_count,
            "total_reports": self.total_reports,
            "max_confidence": self.max_confidence,
        }
