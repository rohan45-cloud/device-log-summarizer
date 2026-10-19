"""Device Log Summarizer CLI.

Usage:
    python main.py --input device_telemetry.csv --output summary.json
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


def clean_sensor_readings(values):
    """Convert valid non-negative values to floats, clipping values above 500."""
    cleaned = []
    for value in values:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if number < 0:
            continue
        cleaned.append(min(number, 500.0))
    return cleaned


def summarize_csv(input_path):
    """Summarize CSV records by device_id."""
    totals = defaultdict(lambda: {"record_count": 0, "temperature_sum": 0.0,
                                  "error_count": 0, "temperature_count": 0})
    required = {"device_id", "status", "temperature"}

    with open(input_path, "r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("CSV must contain device_id, status, and temperature columns.")

        for line_number, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            raw_temperature = row.get("temperature")

            if not device_id:
                print(f"Warning: skipping row {line_number}: missing device_id.", file=sys.stderr)
                continue
            try:
                temperature = float(raw_temperature)
            except (TypeError, ValueError):
                print(f"Warning: skipping row {line_number}: invalid temperature.", file=sys.stderr)
                continue

            if not (temperature == temperature and abs(temperature) != float("inf")):
                print(f"Warning: skipping row {line_number}: non-finite temperature.", file=sys.stderr)
                continue

            entry = totals[device_id]
            entry["record_count"] += 1
            entry["temperature_sum"] += temperature
            entry["temperature_count"] += 1
            if status == "ERROR":
                entry["error_count"] += 1

    results = []
    for device_id, entry in sorted(totals.items()):
        average = entry["temperature_sum"] / entry["temperature_count"]
        if average <= 80.0:
            results.append({
                "device_id": device_id,
                "record_count": entry["record_count"],
                "average_temperature": round(average, 2),
                "error_count": entry["error_count"],
            })
    return results


def print_table(results):
    """Print a simple aligned summary table."""
    headers = ("DEVICE", "RECORDS", "AVG TEMP", "ERRORS")
    rows = [[r["device_id"], str(r["record_count"]),
             f'{r["average_temperature"]:.2f}', str(r["error_count"])]
            for r in results]
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) if rows
              else len(headers[i]) for i in range(len(headers))]
    line = "-+-".join("-" * width for width in widths)
    print(" | ".join(headers[i].ljust(widths[i]) for i in range(4)))
    print(line)
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(4)))
    if not rows:
        print("(No devices met the average-temperature filter.)")


def main():
    parser = argparse.ArgumentParser(description="Summarize device telemetry CSV data.")
    parser.add_argument("--input", default="device_telemetry.csv", help="Input CSV path")
    parser.add_argument("--output", default="summary.json", help="Output JSON path")
    args = parser.parse_args()

    try:
        results = summarize_csv(args.input)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as json_file:
            json.dump(results, json_file, indent=2)
        print_table(results)
        print(f"\nSaved {len(results)} device summaries to {output_path}.")
    except FileNotFoundError:
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
