from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from backend.schemas.common import BilingualMessage

class UserBase(BaseModel):
    phone: str
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    preferred_language: str = "en"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    message: BilingualMessage
