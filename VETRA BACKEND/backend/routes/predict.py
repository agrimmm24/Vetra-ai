from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.schemas.health_input import DailyHealthInput
from backend.schemas.risk_output import RiskAssessment
from backend.services.feature_engineering import engineer_features, get_feature_vector
from backend.services.prediction import prediction_service
from backend.services.rule_engine import evaluate_rules, calculate_health_state
from backend.services.risk_fusion import fuse_risk_scores, get_suggested_actions
from backend.services.explainability import explain_risk, get_explanation_reasons
from backend.models import Animal, HealthRecord, User as UserTable
from sqlalchemy import select
from datetime import datetime
from backend.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=RiskAssessment)
async def predict_risk(
    data: DailyHealthInput, 
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    # 1. Fetch Animal Profile
    result = await db.execute(select(Animal).where(Animal.id == data.animal_id))
    animal = result.scalar_one_or_none()
    
    baseline_milk = animal.baseline_milk if animal else 20.0
    
    # 2. Extract Features
    features = engineer_features(data, baseline_milk=baseline_milk)
    
    # 3. Calculate 3D Health State (Worst-Case Logic)
    h_state = calculate_health_state(
        temperature=data.temperature,
        milk_yield=data.milk_yield or 0.0,
        feed_intake=data.feed_intake
    )
    health_rank = h_state["health_rank"]
    
    # 4. Get Scores
    ml_score = prediction_service.predict(get_feature_vector(features))
    # Pass raw data for user-defined thresholds
    rule_score, rule_reasons = evaluate_rules(features, raw_input=data.model_dump())
    
    # 5. Fuse & Classify
    final_score, risk_level = fuse_risk_scores(rule_score, ml_score)
    
    # 6. Explainability
    importance = explain_risk(features, ml_score)
    explanation_reasons = get_explanation_reasons(features)
    
    # Combine reasons and ensure uniqueness
    seen = set()
    all_reasons = []
    for r in rule_reasons + explanation_reasons:
        if r.en not in seen:
            all_reasons.append(r)
            seen.add(r.en)
    
    # 7. Suggested Actions
    actions = get_suggested_actions(risk_level, all_reasons)

    # 8. Persist to DB
    new_record = HealthRecord(
        animal_id=data.animal_id,
        milk_yield=data.milk_yield,
        feed_intake=data.feed_intake,
        activity_level=data.activity_level,
        temperature=data.temperature,
        risk_score=final_score,
        risk_level=risk_level,
        ph=data.pH,
        heart_rate=data.heart_rate
    )
    db.add(new_record)
    await db.commit()

    return RiskAssessment(
        animal_id=data.animal_id,
        score=final_score,
        level=risk_level,
        health_rank=health_rank,
        reasons=all_reasons,
        actions=actions,
        feature_importance=importance,
        timestamp=datetime.now()
    )
