# Traffic Counter

A program that reads traffic counter data and produces summary statistics.

## Project Structure

```
traffic-counter/
├── src/
│   ├── models.py          # TrafficRecord dataclass
│   ├── loader.py          # File loading/parsing
│   ├── calculators.py     # All calculation functions
│   └── __init__.py
├── tests/
│   ├── test_models.py
│   ├── test_loader.py
│   └── test_calculators.py
├── data/
│   └── sample_input.txt
├── main.py                # Entry point
└── README.md
```

## Usage

```bash
cd traffic-counter
python main.py
```

## Running Tests

```bash
cd traffic-counter
python -m pytest tests/ -v
```

## Input Format

Each line contains a timestamp in ISO 8601 format (`yyyy-mm-ddThh:mm:ss`) followed by a space and the number of cars counted in that half-hour period:

```
2021-12-01T05:00:00 5
2021-12-01T05:30:00 12
```

## Output

The program outputs:

1. **Total cars** seen across all records
2. **Daily totals** — one line per day with date and count
3. **Top 3 half hours** — the three busiest half-hour periods
4. **Least busy 1.5 hours** — three contiguous half-hour records with the fewest cars

### Sample Output

```
Total cars: 398

Cars per day:
2021-12-01 179
2021-12-05 81
2021-12-08 134
2021-12-09 4

Top 3 half hours:
2021-12-01T07:30:00 46
2021-12-01T08:00:00 42
2021-12-08T18:00:00 33

Least busy 1.5 hour period:
2021-12-01T15:00:00 9
2021-12-01T15:30:00 11
2021-12-01T23:30:00 0
```
