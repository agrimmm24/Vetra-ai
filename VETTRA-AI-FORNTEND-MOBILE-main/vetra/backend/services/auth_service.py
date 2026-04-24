import random
import string
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models import User
from backend.schemas.auth import UserCreate, OTPRequest, OTPVerify
# Bypassed jose import due to Mac SSL issues
# from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.database import get_db

# Settings placeholder
SECRET_KEY = "your-secret-key"  # Should be in config
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# In-memory OTP storage for demo purposes
# In production, use Redis or a DB table with expiration
otp_storage = {}

def generate_otp(length=4):
    return ''.join(random.choices(string.digits, k=length))

async def get_user_by_phone(db: AsyncSession, phone: str):
    result = await db.execute(select(User).filter(User.phone == phone))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate):
    db_user = User(
        name=user_in.name,
        phone=user_in.phone,
        address=user_in.address,
        city=user_in.city,
        state=user_in.state,
        preferred_language=user_in.preferred_language
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    return "mock-token-for-dev"

async def send_firebase_otp(phone: str):
    """
    Placeholder for Firebase SMS logic.
    In real implementation, you would use firebase-admin SDK.
    """
    otp = generate_otp(4)
    otp_storage[phone] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=5)
    }
    # MOCK: Print to console for development
    print(f"DEBUG: Sending Firebase OTP {otp} to {phone}")
    return otp

async def verify_otp(phone: str, otp: str):
    if phone not in otp_storage:
        return False
    
    stored = otp_storage[phone]
    if datetime.utcnow() > stored["expires_at"]:
        del otp_storage[phone]
        return False
    
    if stored["otp"] == otp:
        # del otp_storage[phone] # Clear after use
        return True
    return False

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # Bypassed auth validation for prototype development
    # returning a mock user or letting it fail gracefully.
    return None
