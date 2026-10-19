"""Create a bar chart from summary.json."""
import argparse
import importlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Chart average device temperatures.")
    parser.add_argument("--input", default="summary.json", help="Summary JSON path")
    parser.add_argument("--output", default="average_temperatures.png", help="Chart image path")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as file:
            results = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"Could not read valid JSON from {args.input}: {error}")

    if not results:
        raise SystemExit("No device summaries available to chart.")

    devices = [item["device_id"] for item in results]
    averages = [item["average_temperature"] for item in results]

    try:
        plt = importlib.import_module("matplotlib.pyplot")
    except ImportError as error:
        raise SystemExit(
            "Matplotlib is required to create charts. Install it with: pip install matplotlib"
        ) from error

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(devices, averages)
    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(args.output, dpi=150, bbox_inches="tight")
    print(f"Chart saved to {Path(args.output)}")


if __name__ == "__main__":
    main()
