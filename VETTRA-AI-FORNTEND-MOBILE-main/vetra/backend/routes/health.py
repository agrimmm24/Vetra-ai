from fastapi import APIRouter
from backend.config import settings
from backend.services.prediction import prediction_service

router = APIRouter()

@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "model_loaded": prediction_service.model is not None,
    }
