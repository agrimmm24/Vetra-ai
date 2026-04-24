def apply_context_weights(features: dict, animal_state: str) -> dict:
    """
    Adjusts the influence (weights) of specific features based on the animal's lifecycle stage.
    
    - Lactating: Uses all signals normally.
    - Dry: Neutralizes milk drop signal and increases sensitivity to behavioral signals.
    """
    weights = {
        "milk_weight": 1.0,
        "feed_weight": 1.0,
        "activity_weight": 1.0,
        "temp_weight": 1.2  # Temperature is always high priority
    }
    
    if animal_state.lower() == "dry":
        # In dry period, milk drop is irrelevant (0 weight)
        weights["milk_weight"] = 0.0
        # Compensate by upweighting feed and activity
        weights["feed_weight"] = 1.5
        weights["activity_weight"] = 1.5
        
    return weights

def calculate_weighted_risk(features: dict, weights: dict) -> float:
    """
    Computes a baseline risk score (0-100) using feature scores and context weights.
    This serves as a bridge between raw stats and ML predictions.
    """
    # Feature scores are designed so that 0 is "bad/risk" and 1 is "good/normal"
    # except for temp_risk and milk_drop which are "1 is bad".
    
    # We invert feed and activity for the sum (1 - score) so high = risk
    raw_scores = {
        "milk": features["milk_drop_pct"],
        "feed": (1.0 - features["feed_score"]),
        "activity": (1.0 - features["activity_score"]),
        "temp": features["temp_risk"]
    }
    
    total_weight = sum(weights.values())
    weighted_sum = (
        raw_scores["milk"] * weights["milk_weight"] +
        raw_scores["feed"] * weights["feed_weight"] +
        raw_scores["activity"] * weights["activity_weight"] +
        raw_scores["temp"] * weights["temp_weight"]
    )
    
    # Normalize to 0-100
    risk_score = (weighted_sum / total_weight) * 100
    return min(100.0, max(0.0, risk_score))
