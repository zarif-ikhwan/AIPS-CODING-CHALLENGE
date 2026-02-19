"""Loading and parsing of traffic data files."""

from datetime import datetime
from typing import List

from .models import TrafficRecord


def load_traffic_data(filepath: str) -> List[TrafficRecord]:
    """Load and parse a traffic data file.

    Each line should contain a timestamp in ISO 8601 format followed by a space
    and the number of cars counted in that half-hour period.

    Args:
        filepath: Path to the traffic data file.

    Returns:
        A list of TrafficRecord objects, in the order they appear in the file.
    """
    records: List[TrafficRecord] = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            timestamp_str, count_str = line.split()
            timestamp = datetime.fromisoformat(timestamp_str)
            count = int(count_str)
            records.append(TrafficRecord(timestamp=timestamp, count=count))

    return records
