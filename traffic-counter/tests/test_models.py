"""Tests for the TrafficRecord model."""

from datetime import datetime, date

from src.models import TrafficRecord


class TestTrafficRecord:
    """Tests for TrafficRecord dataclass."""

    def test_creation(self):
        record = TrafficRecord(
            timestamp=datetime(2021, 12, 1, 5, 0, 0), count=5
        )
        assert record.timestamp == datetime(2021, 12, 1, 5, 0, 0)
        assert record.count == 5

    def test_date_property(self):
        record = TrafficRecord(
            timestamp=datetime(2021, 12, 1, 5, 30, 0), count=12
        )
        assert record.date == date(2021, 12, 1)

    def test_date_property_midnight(self):
        record = TrafficRecord(
            timestamp=datetime(2021, 12, 9, 0, 0, 0), count=4
        )
        assert record.date == date(2021, 12, 9)

    def test_str_representation(self):
        record = TrafficRecord(
            timestamp=datetime(2021, 12, 1, 5, 0, 0), count=5
        )
        assert str(record) == "2021-12-01T05:00:00 5"

    def test_frozen(self):
        record = TrafficRecord(
            timestamp=datetime(2021, 12, 1, 5, 0, 0), count=5
        )
        try:
            record.count = 10
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass

    def test_equality(self):
        r1 = TrafficRecord(timestamp=datetime(2021, 12, 1, 5, 0, 0), count=5)
        r2 = TrafficRecord(timestamp=datetime(2021, 12, 1, 5, 0, 0), count=5)
        assert r1 == r2

    def test_inequality(self):
        r1 = TrafficRecord(timestamp=datetime(2021, 12, 1, 5, 0, 0), count=5)
        r2 = TrafficRecord(timestamp=datetime(2021, 12, 1, 5, 0, 0), count=10)
        assert r1 != r2
