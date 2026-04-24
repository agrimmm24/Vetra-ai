from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes import predict, simulate, animals, health, auth
from backend.database import engine, Base
# Explicitly import models to ensure registration on Base.metadata
from backend.models import Animal, HealthRecord, User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Database
    async with engine.begin() as conn:
        # This will create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown logic (if any) here

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(predict.router, prefix=f"{settings.API_V1_STR}/predict", tags=["prediction"])
app.include_router(simulate.router, prefix=f"{settings.API_V1_STR}/simulate", tags=["simulation"])
app.include_router(animals.router, prefix=f"{settings.API_V1_STR}/animals", tags=["animals"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to VETTRA-AI LHIS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
