from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from api.dependencies import simulation_manager

router = APIRouter()

@router.get("/")
async def list_personas():
    # Return all personas from all active simulations
    personas = []
    for sim in simulation_manager.simulations.values():
        for p in sim.personas:
            personas.append({
                "name": p.name,
                "simulation_id": sim.id,
                "bio": p.minibio(extended=False)
            })
    return personas
