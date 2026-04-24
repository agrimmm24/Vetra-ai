from pydantic import BaseModel, Field
from typing import List, Literal, Dict
from datetime import datetime
from backend.schemas.common import BilingualMessage

class RiskAssessment(BaseModel):
    animal_id: str
    score: float = Field(..., ge=0, le=100, serialization_alias="score")
    level: Literal["LOW", "MEDIUM", "HIGH"] = Field(..., serialization_alias="level")
    health_rank: Literal["normal", "healthy", "warning", "critical"] = Field(..., description="Overall state for 3D model")
    reasons: List[BilingualMessage] = Field(default_factory=list)
    actions: List[BilingualMessage] = Field(default_factory=list)
    feature_importance: Dict[str, float] = Field(default_factory=dict, description="SHAP-based feature importance breakdown")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "animal_id": "COW-12",
                "score": 72.5,
                "level": "HIGH",
                "health_rank": "warning",
                "reasons": [{"en": "Drop in milk", "hi": "दूध कम है"}],
                "actions": [{"en": "Call vet", "hi": "डॉक्टर को बुलाएँ"}],
                "feature_importance": {"milk_yield": 0.45, "temperature": 0.35},
                "timestamp": "2024-04-18T10:30:00Z"
            }
        }
