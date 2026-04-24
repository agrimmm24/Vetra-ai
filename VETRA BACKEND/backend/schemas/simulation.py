from pydantic import BaseModel, Field
from typing import List, Dict
from backend.schemas.health_input import DailyHealthInput

class SimulationRequest(BaseModel):
    animal_id: str
    modified_inputs: DailyHealthInput

class SimulationResponse(BaseModel):
    before_score: float
    after_score: float
    delta: float = Field(..., description="Change in risk score (simulated - original)")
    risk_level_before: str
    risk_level_after: str
    improved_factors: List[str] = Field(default_factory=list, description="List of factors that improved the risk score")

    class Config:
        json_schema_extra = {
            "example": {
                "original_score": 75.0,
                "simulated_score": 52.0,
                "delta": -23.0,
                "risk_level_before": "HIGH",
                "risk_level_after": "MEDIUM",
                "improved_factors": ["feed_intake", "activity_level"]
            }
        }
