from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.schemas.auth import UserCreate, OTPRequest, OTPVerify, Token, UserResponse, BilingualMessage
from backend.services import auth_service
from datetime import timedelta

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await auth_service.get_user_by_phone(db, user_in.phone)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail={
                "en": "Phone number already registered",
                "hi": "फ़ोन नंबर पहले से ही पंजीकृत है"
            }
        )
    return await auth_service.create_user(db, user_in)

@router.post("/login/request-otp")
async def request_otp(payload: OTPRequest, db: AsyncSession = Depends(get_db)):
    db_user = await auth_service.get_user_by_phone(db, payload.phone)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail={
                "en": "User not found. Please sign up first.",
                "hi": "उपयोगकर्ता नहीं मिला। कृपया पहले साइन अप करें।"
            }
        )
    
    await auth_service.send_firebase_otp(payload.phone)
    return {
        "message": {
            "en": "OTP sent successfully via Firebase",
            "hi": "ओटीपी फायरबेस के माध्यम से सफलतापूर्वक भेजा गया"
        }
    }

@router.post("/login/verify-otp", response_model=Token)
async def verify_otp(payload: OTPVerify, db: AsyncSession = Depends(get_db)):
    is_valid = await auth_service.verify_otp(payload.phone, payload.otp)
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail={
                "en": "Invalid or expired OTP",
                "hi": "अमान्य या समाप्त ओटीपी"
            }
        )
    
    db_user = await auth_service.get_user_by_phone(db, payload.phone)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": db_user.phone}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user,
        "message": {
            "en": "Login successful",
            "hi": "लॉगिन सफल"
        }
    }
