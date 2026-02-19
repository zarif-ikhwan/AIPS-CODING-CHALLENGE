"""Tests for the traffic data loader."""

import tempfile
import os
from datetime import datetime

from src.loader import load_traffic_data
from src.models import TrafficRecord


class TestLoadTrafficData:
    """Tests for load_traffic_data function."""

    def _write_temp_file(self, content: str) -> str:
        """Write content to a temporary file and return its path."""
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path

    def test_load_single_record(self):
        path = self._write_temp_file("2021-12-01T05:00:00 5\n")
        try:
            records = load_traffic_data(path)
            assert len(records) == 1
            assert records[0] == TrafficRecord(
                timestamp=datetime(2021, 12, 1, 5, 0, 0), count=5
            )
        finally:
            os.unlink(path)

    def test_load_multiple_records(self):
        content = (
            "2021-12-01T05:00:00 5\n"
            "2021-12-01T05:30:00 12\n"
            "2021-12-01T06:00:00 14\n"
        )
        path = self._write_temp_file(content)
        try:
            records = load_traffic_data(path)
            assert len(records) == 3
            assert records[0].count == 5
            assert records[1].count == 12
            assert records[2].count == 14
        finally:
            os.unlink(path)

    def test_load_empty_file(self):
        path = self._write_temp_file("")
        try:
            records = load_traffic_data(path)
            assert records == []
        finally:
            os.unlink(path)

    def test_load_ignores_blank_lines(self):
        content = (
            "2021-12-01T05:00:00 5\n"
            "\n"
            "2021-12-01T05:30:00 12\n"
            "\n"
        )
        path = self._write_temp_file(content)
        try:
            records = load_traffic_data(path)
            assert len(records) == 2
        finally:
            os.unlink(path)

    def test_load_preserves_order(self):
        content = (
            "2021-12-05T09:30:00 18\n"
            "2021-12-01T05:00:00 5\n"
        )
        path = self._write_temp_file(content)
        try:
            records = load_traffic_data(path)
            assert records[0].timestamp == datetime(2021, 12, 5, 9, 30, 0)
            assert records[1].timestamp == datetime(2021, 12, 1, 5, 0, 0)
        finally:
            os.unlink(path)

    def test_load_zero_count(self):
        path = self._write_temp_file("2021-12-01T23:30:00 0\n")
        try:
            records = load_traffic_data(path)
            assert records[0].count == 0
        finally:
            os.unlink(path)

    def test_load_sample_input(self):
        """Test loading the provided sample input file."""
        sample_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "sample_input.txt"
        )
        records = load_traffic_data(sample_path)
        assert len(records) == 24
