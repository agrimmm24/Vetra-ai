from datetime import datetime

def format_timestamp(dt: datetime) -> str:
    """
    Standardizes timestamp formatting for API responses.
    """
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def clamp_value(val: float, min_val: float, max_val: float) -> float:
    """
    Clamps a numeric value between a minimum and maximum range.
    """
    return max(min_val, min(max_val, val))

def map_categorical_score(label: str) -> float:
    """
    Helper to map low/medium/high labels to numeric scores.
    """
    mapping = {
        "low": 0.0,
        "medium": 0.5,
        "high": 1.0
    }
    return mapping.get(label.lower(), 0.5)
