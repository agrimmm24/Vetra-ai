import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "VETTRA-AI LHIS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Connection Config for Frontend
    SERVER_HOST: str = "192.168.137.1"
    SERVER_PORT: int = 8000
    API_URL: str = f"http://{SERVER_HOST}:{SERVER_PORT}{API_V1_STR}"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./lhis.db")
    
    # ML Models
    MODEL_PATH: str = os.getenv("MODEL_PATH", "backend/models/trained/random_forest_model.pkl")
    
    class Config:
        case_sensitive = True

settings = Settings()
