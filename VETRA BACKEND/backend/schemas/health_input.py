from pydantic import BaseModel, Field
from typing import Literal, Optional

class DailyHealthInput(BaseModel):
    animal_id: str = Field(..., description="Unique identifier for the animal")
    milk_yield: Optional[float] = Field(None, ge=0, description="Daily milk yield in liters (optional for dry cows)")
    feed_intake: Literal["low", "medium", "high"] = Field(..., description="Daily feed intake level")
    activity_level: Literal["low", "medium", "high"] = Field(..., description="Daily physical activity level")
    temperature: float = Field(..., ge=10.0, le=60.0, description="Animal body temperature in Celsius")
    pH: Optional[float] = Field(None, ge=3.0, le=9.0, description="Milk pH level")
    heart_rate: Optional[float] = Field(None, ge=30.0, le=150.0, description="Animal heart rate (bpm)")

    class Config:
        json_schema_extra = {
            "example": {
                "animal_id": "COW-12",
                "milk_yield": 15.5,
                "feed_intake": "medium",
                "activity_level": "low",
                "temperature": 39.2,
                "pH": 6.6,
                "heart_rate": 72.0
            }
        }
