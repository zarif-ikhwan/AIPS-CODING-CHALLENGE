"""Tests for the calculator functions."""

from datetime import datetime, date

import pytest

from src.models import TrafficRecord
from src.calculators import (
    calculate_total_cars,
    calculate_daily_totals,
    calculate_top_periods,
    calculate_least_contiguous_period,
)


def _record(date_str: str, time_str: str, count: int) -> TrafficRecord:
    """Helper to create a TrafficRecord from date/time strings."""
    return TrafficRecord(
        timestamp=datetime.fromisoformat(f"{date_str}T{time_str}"),
        count=count,
    )


# --- Sample data fixtures ---

SAMPLE_RECORDS = [
    _record("2021-12-01", "05:00:00", 5),
    _record("2021-12-01", "05:30:00", 12),
    _record("2021-12-01", "06:00:00", 14),
    _record("2021-12-01", "06:30:00", 15),
    _record("2021-12-01", "07:00:00", 25),
    _record("2021-12-01", "07:30:00", 46),
    _record("2021-12-01", "08:00:00", 42),
    _record("2021-12-01", "15:00:00", 9),
    _record("2021-12-01", "15:30:00", 11),
    _record("2021-12-01", "23:30:00", 0),
    _record("2021-12-05", "09:30:00", 18),
    _record("2021-12-05", "10:30:00", 15),
    _record("2021-12-05", "11:30:00", 7),
    _record("2021-12-05", "12:30:00", 6),
    _record("2021-12-05", "13:30:00", 9),
    _record("2021-12-05", "14:30:00", 11),
    _record("2021-12-05", "15:30:00", 15),
    _record("2021-12-08", "18:00:00", 33),
    _record("2021-12-08", "19:00:00", 28),
    _record("2021-12-08", "20:00:00", 25),
    _record("2021-12-08", "21:00:00", 21),
    _record("2021-12-08", "22:00:00", 16),
    _record("2021-12-08", "23:00:00", 11),
    _record("2021-12-09", "00:00:00", 4),
]


# === calculate_total_cars ===


class TestCalculateTotalCars:
    def test_empty_list(self):
        assert calculate_total_cars([]) == 0

    def test_single_record(self):
        records = [_record("2021-12-01", "05:00:00", 5)]
        assert calculate_total_cars(records) == 5

    def test_sample_data(self):
        assert calculate_total_cars(SAMPLE_RECORDS) == 398

    def test_includes_zero_counts(self):
        records = [
            _record("2021-12-01", "05:00:00", 0),
            _record("2021-12-01", "05:30:00", 10),
        ]
        assert calculate_total_cars(records) == 10


# === calculate_daily_totals ===


class TestCalculateDailyTotals:
    def test_empty_list(self):
        assert calculate_daily_totals([]) == {}

    def test_single_day(self):
        records = [
            _record("2021-12-01", "05:00:00", 5),
            _record("2021-12-01", "05:30:00", 12),
        ]
        result = calculate_daily_totals(records)
        assert result == {date(2021, 12, 1): 17}

    def test_multiple_days(self):
        result = calculate_daily_totals(SAMPLE_RECORDS)
        assert result[date(2021, 12, 1)] == 179
        assert result[date(2021, 12, 5)] == 81
        assert result[date(2021, 12, 8)] == 134
        assert result[date(2021, 12, 9)] == 4

    def test_preserves_order(self):
        result = calculate_daily_totals(SAMPLE_RECORDS)
        dates = list(result.keys())
        assert dates == [
            date(2021, 12, 1),
            date(2021, 12, 5),
            date(2021, 12, 8),
            date(2021, 12, 9),
        ]


# === calculate_top_periods ===


class TestCalculateTopPeriods:
    def test_top_3_sample_data(self):
        top3 = calculate_top_periods(SAMPLE_RECORDS, n=3)
        assert len(top3) == 3
        assert top3[0].count == 46
        assert top3[1].count == 42
        assert top3[2].count == 33

    def test_top_1(self):
        top1 = calculate_top_periods(SAMPLE_RECORDS, n=1)
        assert len(top1) == 1
        assert top1[0].count == 46
        assert top1[0].timestamp == datetime(2021, 12, 1, 7, 30, 0)

    def test_empty_list(self):
        assert calculate_top_periods([], n=3) == []

    def test_fewer_records_than_n(self):
        records = [
            _record("2021-12-01", "05:00:00", 5),
            _record("2021-12-01", "05:30:00", 12),
        ]
        result = calculate_top_periods(records, n=3)
        assert len(result) == 2

    def test_preserves_correct_timestamps(self):
        top3 = calculate_top_periods(SAMPLE_RECORDS, n=3)
        assert top3[0].timestamp == datetime(2021, 12, 1, 7, 30, 0)
        assert top3[1].timestamp == datetime(2021, 12, 1, 8, 0, 0)
        assert top3[2].timestamp == datetime(2021, 12, 8, 18, 0, 0)


# === calculate_least_contiguous_period ===


class TestCalculateLeastContiguousPeriod:
    def test_sample_data_window_3(self):
        result = calculate_least_contiguous_period(SAMPLE_RECORDS, window=3)
        assert len(result) == 3
        total = sum(r.count for r in result)
        # The least 1.5-hour period should be the minimum sum of 3 contiguous records
        # Verify by brute force
        min_total = min(
            sum(r.count for r in SAMPLE_RECORDS[i : i + 3])
            for i in range(len(SAMPLE_RECORDS) - 2)
        )
        assert total == min_total

    def test_specific_least_period(self):
        """The least busy 1.5h window in sample data is records with counts 0, 18, 15 = 33
        or 7, 6, 9 = 22. Let's verify."""
        result = calculate_least_contiguous_period(SAMPLE_RECORDS, window=3)
        counts = [r.count for r in result]
        total = sum(counts)
        # Check all windows to find actual minimum
        all_windows = [
            sum(r.count for r in SAMPLE_RECORDS[i : i + 3])
            for i in range(len(SAMPLE_RECORDS) - 2)
        ]
        assert total == min(all_windows)

    def test_window_equals_list_length(self):
        records = [
            _record("2021-12-01", "05:00:00", 5),
            _record("2021-12-01", "05:30:00", 12),
            _record("2021-12-01", "06:00:00", 14),
        ]
        result = calculate_least_contiguous_period(records, window=3)
        assert len(result) == 3
        assert sum(r.count for r in result) == 31

    def test_raises_on_insufficient_records(self):
        records = [
            _record("2021-12-01", "05:00:00", 5),
            _record("2021-12-01", "05:30:00", 12),
        ]
        with pytest.raises(ValueError):
            calculate_least_contiguous_period(records, window=3)

    def test_empty_list_raises(self):
        with pytest.raises(ValueError):
            calculate_least_contiguous_period([], window=3)

    def test_custom_window_size(self):
        records = [
            _record("2021-12-01", "05:00:00", 10),
            _record("2021-12-01", "05:30:00", 1),
            _record("2021-12-01", "06:00:00", 2),
            _record("2021-12-01", "06:30:00", 20),
        ]
        result = calculate_least_contiguous_period(records, window=2)
        assert len(result) == 2
        assert sum(r.count for r in result) == 3
        assert result[0].count == 1
        assert result[1].count == 2
