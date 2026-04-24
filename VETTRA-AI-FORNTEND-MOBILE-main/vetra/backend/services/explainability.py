from typing import Dict, List, Any
import numpy as np
from backend.schemas.common import BilingualMessage

def explain_risk(features: dict, ml_score: float) -> Dict[str, Any]:
    """
    Simulates SHAP (SHapley Additive exPlanations) to identify feature importance
    and map them to human-readable reasons.
    """
    # In a real scenario, we would use shap.TreeExplainer(model)
    # Here we calculate relative impacts based on deviations from 'normal'
    
    impacts = {
        "milk_yield": features["milk_drop_pct"] * 2.0,
        "feed_intake": (1.0 - features["feed_score"]) * 1.5,
        "activity_level": (1.0 - features["activity_score"]) * 1.5,
        "temperature": features["temp_risk"] * 2.5
    }
    
    # Normalize impacts to sum to 1.0 (relative importance)
    total = sum(impacts.values())
    if total > 0:
        importance = {k: v/total for k, v in impacts.items()}
    else:
        importance = {k: 0.0 for k in impacts.keys()}
        
    return importance

def get_explanation_reasons(features: dict) -> List[BilingualMessage]:
    """
    Translates feature states into human-readable alerts.
    """
    reasons = []
    
    if features["milk_drop_pct"] > 0.10:
        pct = features['milk_drop_pct']*100
        reasons.append(BilingualMessage(
            en=f"Milk yield has decreased by {pct:.1f}% from baseline.",
            hi=f"दूध की पैदावार बेसलाइन से {pct:.1f}% कम हो गई है।"
        ))
        
    if features["feed_score"] < 0.5:
        reasons.append(BilingualMessage(
            en="Feed intake is below normal levels.",
            hi="पशु का चारा खाना सामान्य स्तर से नीचे है।"
        ))
        
    if features["activity_score"] < 0.5:
        reasons.append(BilingualMessage(
            en="Animal activity is lower than average.",
            hi="पशु की गतिविधि सामान्य से कम है।"
        ))
        
    if features["temp_risk"] >= 0.5:
        reasons.append(BilingualMessage(
            en="Body temperature is elevated, indicating possible stress or illness.",
            hi="शरीर का तापमान बढ़ गया है, जो तनाव या बीमारी का संकेत दे सकता है।"
        ))

    if "ph_score" in features and features["ph_score"] > 0.5:
        reasons.append(BilingualMessage(
            en="Milk pH is abnormal, indicating potential mastitis risk.",
            hi="दूध का पीएच असामान्य है, जो संभावित थनैला (मैस्टाइटिस) जोखिम का संकेत देता है।"
        ))

    if "hr_score" in features and features["hr_score"] > 0.5:
        reasons.append(BilingualMessage(
            en="Heart rate is elevated, suggesting fever or physical distress.",
            hi="हृदय गति तेज है, जो बुखार या शारीरिक संकट का संकेत देती है।"
        ))
        
    return reasons
