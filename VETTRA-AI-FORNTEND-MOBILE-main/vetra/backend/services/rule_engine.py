from typing import List, Tuple, Dict
from backend.schemas.common import BilingualMessage

def calculate_health_state(
    temperature: float, 
    milk_yield: float, 
    feed_intake: str
) -> Dict[str, any]:
    """
    Calculates individual states for Temp, Milk, and Feed.
    Returns the WORST case scenario as the final health rank.
    """
    states = {
        "normal": 0,
        "healthy": 1,
        "warning": 2,
        "critical": 3
    }
    reverse_states = {v: k for k, v in states.items()}
    
    # 1. Temperature State
    if temperature <= 20.0:
        temp_state = states["normal"]
    elif temperature <= 39.0:
        temp_state = states["healthy"]
    elif temperature <= 55.0:
        temp_state = states["warning"]
    else:
        temp_state = states["critical"]
        
    # 2. Milk Yield State
    if milk_yield >= 25.0:
        milk_state = states["normal"]
    elif milk_yield >= 15.0:
        milk_state = states["healthy"]
    elif milk_yield >= 10.0:
        milk_state = states["warning"]
    else:
        milk_state = states["critical"]
        
    # 3. Feed Intake State
    feed_map = {
        "high": states["normal"],
        "medium": states["healthy"],
        "low": states["critical"]
    }
    feed_state = feed_map.get(feed_intake.lower(), states["healthy"])
    
    # Worst Case Logic
    worst_val = max(temp_state, milk_state, feed_state)
    health_rank = reverse_states[worst_val]
    
    return {
        "health_rank": health_rank,
        "individual_states": {
            "temp": reverse_states[temp_state],
            "milk": reverse_states[milk_state],
            "feed": reverse_states[feed_state]
        }
    }

def evaluate_rules(features: dict, raw_input: dict = None) -> Tuple[float, List[BilingualMessage]]:
    """
    Evaluates veterinary rules and returns a score and bilingual reasons.
    """
    reasons = []
    points = 0
    
    # Using raw_input if available for more precise user-defined rules
    if raw_input:
        temp = raw_input.get("temperature", 38.5)
        milk = raw_input.get("milk_yield", 20.0)
        feed = raw_input.get("feed_intake", "medium")
        
        # Threshold-based reasons
        if temp > 40.0:
            points += 30
            reasons.append(BilingualMessage(
                en="Abnormally high body temperature detected.",
                hi="शरीर का तापमान असामान्य रूप से अधिक पाया गया।"
            ))
        elif temp < 37.0:
            points += 20
            reasons.append(BilingualMessage(
                en="Body temperature is lower than normal.",
                hi="शरीर का तापमान सामान्य से कम है।"
            ))
            
        if milk < 10.0:
            points += 30
            reasons.append(BilingualMessage(
                en="Critical drop in milk production.",
                hi="दूध उत्पादन में भारी गिरावट।"
            ))
            
        if feed == "low":
            points += 25
            reasons.append(BilingualMessage(
                en="Low feed intake reported.",
                hi="पशु का चारा खाना कम हो गया है।"
            ))

    # Fallback to feature-based rules for points if needed
    if not reasons:
        if features.get("milk_drop_pct", 0) > 0.15:
            points += 20
        if features.get("temp_risk", 0) >= 0.5:
            points += 20

    return min(100.0, float(points)), reasons
