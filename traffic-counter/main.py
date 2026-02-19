"""Entry point for the traffic counter program."""

from pathlib import Path

from src.loader import load_traffic_data
from src.calculators import (
    calculate_total_cars,
    calculate_daily_totals,
    calculate_top_periods,
    calculate_least_contiguous_period,
)


def format_output(filepath: str) -> str:
    """Run all analyses and return formatted output.

    Args:
        filepath: Path to the traffic data file.

    Returns:
        Formatted string containing all output sections.
    """
    records = load_traffic_data(filepath)

    lines: list[str] = []

    # Total cars
    total = calculate_total_cars(records)
    lines.append(f"Total cars: {total}")
    lines.append("")

    # Daily totals
    lines.append("Cars per day:")
    daily = calculate_daily_totals(records)
    for day, count in daily.items():
        lines.append(f"{day} {count}")
    lines.append("")

    # Top 3 half-hour periods
    lines.append("Top 3 half hours:")
    top3 = calculate_top_periods(records, n=3)
    for record in top3:
        lines.append(str(record))
    lines.append("")

    # Least busy 1.5-hour period
    lines.append("Least busy 1.5 hour period:")
    least = calculate_least_contiguous_period(records, window=3)
    for record in least:
        lines.append(str(record))

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    filepath = str(Path(__file__).parent / "data" / "sample_input.txt")
    print(format_output(filepath))


if __name__ == "__main__":
    main()
