from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.schemas.simulation import SimulationRequest, SimulationResponse
from backend.services.simulation import run_risk_simulation
from backend.models import Animal, User as UserTable
from backend.services.auth_service import get_current_user
from sqlalchemy import select

router = APIRouter()

@router.post("/", response_model=SimulationResponse)
async def simulate_scenario(
    data: SimulationRequest, 
    db: AsyncSession = Depends(get_db)
):
    # Fetch animal state
    result = await db.execute(select(Animal).where(Animal.id == data.animal_id))
    animal = result.scalar_one_or_none()
    
    animal_state = animal.state if animal else "lactating"
    
    # We don't have the 'original' input in the request, in a real app 
    # we might fetch the LATEST record from the DB for this animal.
    # For now, we assume the modified_inputs contains the baseline as well 
    # or handle it as a comparison between two theoretical states.
    
    # Mocking 'original' as a slightly worse version of modified for demonstration
    # In production, this would be fetched from HealthRecord
    original_input = data.modified_inputs.model_copy()
    original_input.temperature += 0.5
    
    response = await run_risk_simulation(
        data.animal_id,
        original_input,
        data.modified_inputs,
        animal_state=animal_state
    )
    
    return response
