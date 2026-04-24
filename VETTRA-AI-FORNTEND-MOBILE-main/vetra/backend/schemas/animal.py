from pydantic import BaseModel
from typing import Literal

class AnimalCreate(BaseModel):
    id: str
    name: str
    breed: str
    age: float
    state: Literal["lactating", "dry"]
    baseline_milk: float = 20.0

class AnimalUpdate(BaseModel):
    name: str = None
    age: float = None
    state: Literal["lactating", "dry"] = None
    baseline_milk: float = None
