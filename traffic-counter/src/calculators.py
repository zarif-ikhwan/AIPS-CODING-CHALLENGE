"""Calculator functions for traffic data analysis."""

from collections import OrderedDict
from datetime import date
from typing import Dict, List

from .models import TrafficRecord


def calculate_total_cars(records: List[TrafficRecord]) -> int:
    """Calculate total number of cars across all records.

    Args:
        records: List of traffic records.

    Returns:
        Total car count.
    """
    return sum(r.count for r in records)


def calculate_daily_totals(records: List[TrafficRecord]) -> Dict[date, int]:
    """Calculate the total number of cars seen on each day.

    Results are returned in the order days first appear in the input.

    Args:
        records: List of traffic records.

    Returns:
        An ordered dict mapping each date to its total car count.
    """
    daily: Dict[date, int] = OrderedDict()
    for record in records:
        daily[record.date] = daily.get(record.date, 0) + record.count
    return daily


def calculate_top_periods(
    records: List[TrafficRecord], n: int = 3
) -> List[TrafficRecord]:
    """Get the top N half-hour periods with the most cars.

    Args:
        records: List of traffic records.
        n: Number of top periods to return.

    Returns:
        A list of up to N TrafficRecords, sorted by count descending.
    """
    return sorted(records, key=lambda r: r.count, reverse=True)[:n]


def calculate_least_contiguous_period(
    records: List[TrafficRecord], window: int = 3
) -> List[TrafficRecord]:
    """Find the contiguous period of `window` half-hour records with the least cars.

    Args:
        records: List of traffic records (assumed to be in chronological order).
        window: Number of contiguous half-hour records in the period.

    Returns:
        A list of TrafficRecords representing the least busy contiguous period.

    Raises:
        ValueError: If fewer records exist than the window size.
    """
    if len(records) < window:
        raise ValueError(
            f"Need at least {window} records, but only got {len(records)}"
        )

    min_total = calculate_total_cars(records[0:window])
    min_start = 0

    for i in range(1, len(records) - window + 1):
        window_total = calculate_total_cars(records[i : i + window])
        if window_total < min_total:
            min_total = window_total
            min_start = i

    return records[min_start : min_start + window]
