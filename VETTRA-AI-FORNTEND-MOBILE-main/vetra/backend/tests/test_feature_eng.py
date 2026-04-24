import pytest
from backend.services.feature_engineering import engineer_features
from backend.schemas.health_input import DailyHealthInput

def test_engineer_features_lactating():
    data = DailyHealthInput(
        animal_id="COW-1",
        milk_yield=15.0,
        feed_intake="medium",
        activity_level="low",
        temperature=39.2
    )
    # baseline 20L
    features = engineer_features(data, baseline_milk=20.0)
    
    # 15/20 drop -> 25% drop
    assert features["milk_drop_pct"] == 0.25
    assert features["feed_score"] == 0.5
    assert features["activity_score"] == 0.0
    assert features["temp_risk"] == 0.5 # 39.2 > 39.0

def test_engineer_features_dry():
    data = DailyHealthInput(
        animal_id="COW-2",
        milk_yield=None, # Dry
        feed_intake="high",
        activity_level="high",
        temperature=38.5
    )
    features = engineer_features(data)
    
    assert features["milk_drop_pct"] == 0.0
    assert features["feed_score"] == 1.0
    assert features["activity_score"] == 1.0
    assert features["temp_risk"] == 0.0
