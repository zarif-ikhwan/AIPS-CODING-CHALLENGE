"""Data models for the traffic counter system."""

from dataclasses import dataclass
from datetime import datetime, date


@dataclass(frozen=True)
class TrafficRecord:
    """Represents a single half-hour traffic count reading."""

    timestamp: datetime
    count: int

    @property
    def date(self) -> date:
        """Extract the date portion of the timestamp."""
        return self.timestamp.date()

    def __str__(self) -> str:
        return f"{self.timestamp.isoformat()} {self.count}"
