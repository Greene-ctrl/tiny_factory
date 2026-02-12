from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import uvicorn

from tinytroupe.simulation_manager import SimulationManager, SimulationConfig
from tinytroupe.agent.social_types import Content

app = FastAPI(title="TinyTroupe Simulation API")

simulation_manager = SimulationManager()

class CreateSimulationRequest(BaseModel):
    name: str
    persona_count: int = 10
    network_type: str = "scale_free"

class RunSimulationRequest(BaseModel):
    content: str
    mode: str = "full"

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/simulations")
async def create_simulation(request: CreateSimulationRequest):
    config = SimulationConfig(
        name=request.name,
        persona_count=request.persona_count,
        network_type=request.network_type
    )
    simulation = simulation_manager.create_simulation(config)
    return {"id": simulation.id, "name": simulation.config.name, "status": simulation.status}

@app.post("/api/v1/simulations/{simulation_id}/run")
async def run_simulation(simulation_id: str, request: RunSimulationRequest):
    content = Content(text=request.content)
    result = simulation_manager.run_simulation(simulation_id, content, mode=request.mode)
    return {
        "total_reach": result.total_reach,
        "expected_likes": result.expected_likes,
        "expected_comments": result.expected_comments,
        "expected_shares": result.expected_shares,
        "execution_time": result.execution_time
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
