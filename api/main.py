from fastapi import FastAPI
from tinytroupe.simulation_manager import SimulationManager

app = FastAPI(title="Tiny Factory & Artificial Societies API")

simulation_manager = SimulationManager()

@app.get("/health")
def health():
    return {"status": "ok"}

# Import routers after app and simulation_manager are defined
from api.routers import simulations, personas
app.include_router(simulations.router, prefix="/api/v1/simulations", tags=["simulations"])
app.include_router(personas.router, prefix="/api/v1/personas", tags=["personas"])
