from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from api.main import simulation_manager
from tinytroupe.simulation_manager import SimulationConfig

router = APIRouter()

class CreateSimulationRequest(BaseModel):
    name: str
    persona_count: int = 10
    network_type: str = "scale_free"

class RunSimulationRequest(BaseModel):
    content: str

class SimulationResponse(BaseModel):
    id: str
    name: str
    status: str
    persona_count: int
    created_at: datetime

@router.post("/", response_model=SimulationResponse)
async def create_simulation(request: CreateSimulationRequest):
    config = SimulationConfig(
        name=request.name,
        persona_count=request.persona_count,
        network_type=request.network_type
    )
    sim = simulation_manager.create_simulation(config)
    return SimulationResponse(
        id=sim.id,
        name=sim.config.name,
        status=sim.status,
        persona_count=len(sim.personas),
        created_at=sim.created_at
    )

@router.post("/{simulation_id}/run")
async def run_simulation(simulation_id: str, request: RunSimulationRequest):
    if simulation_id not in simulation_manager.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    result = simulation_manager.run_simulation(simulation_id, request.content)
    return {
        "simulation_id": simulation_id,
        "total_reach": result.total_reach,
        "engagement_count": len(result.engagements)
    }
