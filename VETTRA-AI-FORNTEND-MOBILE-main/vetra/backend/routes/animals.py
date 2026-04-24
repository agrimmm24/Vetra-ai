from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.models import Animal, User as UserTable
from backend.services.auth_service import get_current_user
from backend.schemas.animal import AnimalCreate, AnimalUpdate
from sqlalchemy import select
from typing import List

router = APIRouter()

@router.get("/", response_model=List[AnimalCreate])
async def list_animals(
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    result = await db.execute(select(Animal))
    return result.scalars().all()

@router.post("/", response_model=AnimalCreate)
async def create_animal(
    animal: AnimalCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    db_animal = Animal(**animal.model_dump())
    db.add(db_animal)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Animal ID already exists")
    return db_animal

@router.get("/{animal_id}", response_model=AnimalCreate)
async def get_animal(
    animal_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    result = await db.execute(select(Animal).where(Animal.id == animal_id))
    db_animal = result.scalar_one_or_none()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return db_animal
