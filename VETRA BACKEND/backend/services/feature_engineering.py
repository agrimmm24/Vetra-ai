import numpy as np
from backend.schemas.health_input import DailyHealthInput

def engineer_features(data: DailyHealthInput, baseline_milk: float = 20.0) -> dict:
    """
    Transforms raw inputs into derived signals for the risk model.
    """
    # 1. Milk Drop Percentage
    # Handle cases where milk might be None (dry cows) or baseline is zero
    if data.milk_yield is not None and baseline_milk > 0:
        milk_drop_pct = (baseline_milk - data.milk_yield) / baseline_milk
        milk_drop_pct = max(0.0, milk_drop_pct)  # Clamp to 0 if yield increases
    else:
        milk_drop_pct = 0.0

    # 2. Categorical Mappings
    map_score = {"low": 0.0, "medium": 0.5, "high": 1.0}
    feed_score = map_score.get(data.feed_intake, 0.5)
    activity_score = map_score.get(data.activity_level, 0.5)

    # 3. Temperature Risk Signaling
    # Normal temp for cows is ~38.5C. Risk starts spiking after 39.5C.
    if data.temperature > 39.5:
        temp_risk = 1.0
    elif data.temperature > 39.0:
        temp_risk = 0.5
    else:
        temp_risk = 0.0

    temp_deviation = abs(data.temperature - 38.5) / 3.5
    temp_deviation = min(1.0, temp_deviation)

    # 5. pH Risk (Normal 6.4 - 6.8)
    if data.pH is not None:
        ph_dev = abs(data.pH - 6.6) / 1.0
        ph_score = min(1.0, ph_dev)
    else:
        ph_score = 0.0

    # 6. Heart Rate Risk (Normal 60-80)
    if data.heart_rate is not None:
        hr_dev = abs(data.heart_rate - 70.0) / 40.0
        hr_score = min(1.0, hr_dev)
    else:
        hr_score = 0.0

    return {
        "milk_drop_pct": milk_drop_pct,
        "feed_score": feed_score,
        "activity_score": activity_score,
        "temp_risk": temp_risk,
        "temp_deviation": temp_deviation,
        "ph_score": ph_score,
        "hr_score": hr_score
    }

def get_feature_vector(features: dict) -> np.ndarray:
    """
    Converts feature dictionary to a flat numpy array for model inference.
    """
    return np.array([
        features["milk_drop_pct"],
        features["feed_score"],
        features["activity_score"],
        features["temp_risk"],
        features["temp_deviation"],
        features["ph_score"],
        features["hr_score"]
    ]).reshape(1, -1)
