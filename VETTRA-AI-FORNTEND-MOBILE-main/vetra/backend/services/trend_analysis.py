from typing import List, Dict
from ..models import HealthRecord

def analyze_milk_trend(records: List[HealthRecord]) -> Dict[str, Any]:
    """
    Analyzes milk yield patterns over the provided records (e.g., last 7 days).
    """
    if len(records) < 2:
        return {"trend": "insufficient_data", "delta": 0.0}
    
    # Sort by date
    sorted_records = sorted(records, key=lambda x: x.date)
    
    yields = [r.milk_yield for r in sorted_records if r.milk_yield is not None]
    
    if len(yields) < 2:
        return {"trend": "insufficient_data", "delta": 0.0}
        
    delta = yields[-1] - yields[0]
    
    if delta < -2.0:  # Threshold for significant drop
        status = "declining"
    elif delta > 2.0:
        status = "improving"
    else:
        status = "stable"
        
    return {
        "status": status,
        "delta": float(delta),
        "days_analyzed": len(yields)
    }

def analyze_risk_trend(records: List[HealthRecord]) -> Dict[str, Any]:
    """
    Analyzes composite risk score patterns.
    """
    if len(records) < 2:
        return {"status": "stable", "delta": 0.0}
        
    sorted_records = sorted(records, key=lambda x: x.date)
    scores = [r.risk_score for r in sorted_records]
    
    delta = scores[-1] - scores[0]
    
    if delta > 10.0:
        status = "increasing_risk"
    elif delta < -10.0:
        status = "decreasing_risk"
    else:
        status = "stable"
        
    return {
        "status": status,
        "delta": float(delta)
    }
