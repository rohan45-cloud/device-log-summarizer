# AI Prompt Log

## Initial prompt
Write a Python script that reads `summary.json` created by my Device Log Summarizer, then uses matplotlib to create a bar chart comparing each device's average temperature. Include a chart title and axis labels.

## Bug or formatting issue reviewed
In an initial draft, long device labels and value labels could overlap or be clipped, and the chart could be saved without enough layout spacing.

## Follow-up prompt
Please improve the chart layout: use a wider figure, add numeric labels above each bar, label both axes, add a light horizontal grid, call `tight_layout()`, and save the figure with `bbox_inches="tight"`. Also handle missing or invalid JSON and an empty result list clearly.

## What I checked
- Reviewed the generated code instead of accepting it blindly.
- Confirmed that the JSON keys match the output from `main.py`.
- Added clear error messages for missing/invalid input and empty summaries.
- Ran the script with the sample CSV and checked the generated chart.

## Note
The CSV included in this project is illustrative sample data because the assessment PDF described `device_telemetry.csv` but did not include the actual data file. Replace it with the employer-provided CSV before final submission.
