import math

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
        if not math.isfinite(number):
            continue
        
        if number < 0:
            continue
        cleaned.append(min(number, 500.0))
    return cleaned