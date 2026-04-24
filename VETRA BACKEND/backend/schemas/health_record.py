from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional

class HealthRecordResponse(BaseModel):
    id: int
    animal_id: str
    date: date
    milk_yield: Optional[float]
    feed_intake: str
    activity_level: str
    temperature: float
    risk_score: float
    risk_level: str
    ph: Optional[float]
    heart_rate: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
