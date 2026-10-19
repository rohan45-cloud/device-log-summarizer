# Device Log Summarizer CLI

A Python command-line tool for summarizing device telemetry records from CSV into JSON, printing a terminal table, and charting average temperatures.

## Requirements
- Python 3.9+
- matplotlib (only needed for charting)

## Run
```bash
python main.py --input device_telemetry.csv --output summary.json
python -m unittest
python -m pip install matplotlib
python chart.py --input summary.json --output average_temperatures.png
```

## Notes
- Devices with average temperature above 80.0 are excluded from the final JSON and table.
- Rows with a missing device ID or invalid/non-finite temperature are skipped with a warning.
- The bundled CSV is sample data. Replace it with the actual assessment CSV if supplied separately.
"# device-log-summarizer" 
