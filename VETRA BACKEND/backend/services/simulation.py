from typing import List, Tuple
from backend.schemas.health_input import DailyHealthInput
from backend.schemas.simulation import SimulationResponse
from backend.services.feature_engineering import engineer_features, get_feature_vector
from backend.services.prediction import prediction_service
from backend.services.rule_engine import evaluate_rules
from backend.services.risk_fusion import fuse_risk_scores

async def run_risk_simulation(
    animal_id: str,
    original_input: DailyHealthInput,
    modified_input: DailyHealthInput,
    animal_state: str = "lactating"
) -> SimulationResponse:
    """
    Simulates the change in risk score by comparing two sets of animal data.
    """
    
    # 1. Process Original Data
    orig_feats = engineer_features(original_input)
    orig_ml_score = prediction_service.predict(get_feature_vector(orig_feats))
    orig_rule_score, _ = evaluate_rules(orig_feats)
    orig_final, orig_level = fuse_risk_scores(orig_rule_score, orig_ml_score)
    
    # 2. Process Modified Data
    mod_feats = engineer_features(modified_input)
    mod_ml_score = prediction_service.predict(get_feature_vector(mod_feats))
    mod_rule_score, _ = evaluate_rules(mod_feats)
    mod_final, mod_level = fuse_risk_scores(mod_rule_score, mod_ml_score)
    
    # 3. Identify Improved Factors
    improved_factors = []
    if modified_input.feed_intake != original_input.feed_intake:
        if orig_feats["feed_score"] < mod_feats["feed_score"]:
            improved_factors.append("feed_intake")
            
    if modified_input.activity_level != original_input.activity_level:
        if orig_feats["activity_score"] < mod_feats["activity_score"]:
            improved_factors.append("activity_level")
            
    if (modified_input.milk_yield or 0) > (original_input.milk_yield or 0):
        improved_factors.append("milk_yield")
        
    if modified_input.temperature < original_input.temperature:
        improved_factors.append("temperature")

    return SimulationResponse(
        before_score=orig_final,
        after_score=mod_final,
        delta=mod_final - orig_final,
        risk_level_before=orig_level,
        risk_level_after=mod_level,
        improved_factors=improved_factors
    )
