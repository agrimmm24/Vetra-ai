from typing import List, Tuple
from backend.schemas.common import BilingualMessage

def fuse_risk_scores(
    rule_score: float, 
    ml_score: float = 0.0, 
    voice_score: float = 0.0
) -> Tuple[float, str]:
    """
    Combines different scoring sources into a single composite risk score.
    
    Weights:
    - Rule Engine: 40%
    - ML Model: 50%
    - Voice Analysis: 10%
    """
    # Weight configuration
    W_RULE = 0.40
    W_ML = 0.50
    W_VOICE = 0.10
    
    # Calculate weighted composite
    composite_score = (
        (rule_score * W_RULE) +
        (ml_score * W_ML) +
        (voice_score * W_VOICE)
    )
    
    # Ensure score stays in 0-100 range
    final_score = min(100.0, max(0.0, composite_score))
    
    # Classify Risk Level
    if final_score >= 70:
        level = "HIGH"
    elif final_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"
        
    return final_score, level

def get_suggested_actions(risk_level: str, triggered_reasons: List[BilingualMessage]) -> List[BilingualMessage]:
    """
    Generates actionable recommendations based on risk intensity and specific triggers.
    """
    actions = []
    
    if risk_level == "HIGH":
        actions.append(BilingualMessage(
            en="Isolate the animal immediately to prevent potential spread.",
            hi="संभावित फैलाव को रोकने के लिए पशु को तुरंत अलग करें।"
        ))
        actions.append(BilingualMessage(
            en="Contact a veterinarian for an urgent physical examination.",
            hi="त्वरित शारीरिक जांच के लिए पशु चिकित्सक से संपर्क करें।"
        ))
        actions.append(BilingualMessage(
            en="Monitor vital signals every 4 hours.",
            hi="हर 4 घंटे में महत्वपूर्ण संकेतों की निगरानी करें।"
        ))
    elif risk_level == "MEDIUM":
        actions.append(BilingualMessage(
            en="Increase frequency of monitoring.",
            hi="निगरानी की आवृत्ति बढ़ाएं।"
        ))
        actions.append(BilingualMessage(
            en="Check feeding area for quality/availability issues.",
            hi="गुणवत्ता/उपलब्धता के मुद्दों के लिए खिला क्षेत्र की जांच करें।"
        ))
        actions.append(BilingualMessage(
            en="Observe behavior for next 24 hours.",
            hi="अगले 24 घंटों के लिए व्यवहार का निरीक्षण करें।"
        ))
    else:
        actions.append(BilingualMessage(
            en="Continue routine daily monitoring.",
            hi="नियमित दैनिक निगरानी जारी रखें।"
        ))
        
    # Context-specific actions
    reason_texts = " ".join([r.en.lower() for r in triggered_reasons])
    if "milk" in reason_texts:
        actions.append(BilingualMessage(
            en="Verify milking equipment hygiene and functionality.",
            hi="दूध निकालने वाले उपकरणों की स्वच्छता और कार्यक्षमता की पुष्टि करें।"
        ))
    if "fever" in reason_texts or "temperature" in reason_texts:
        actions.append(BilingualMessage(
            en="Ensure access to clean water and shaded resting area.",
            hi="स्वच्छ पानी और छायादार विश्राम क्षेत्र तक पहुंच सुनिश्चित करें।"
        ))
        
    return actions
