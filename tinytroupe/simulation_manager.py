from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import json
from tinytroupe.agent.tiny_person import TinyPerson
from tinytroupe.social_network import NetworkTopology
from tinytroupe.environment.social_world import SocialTinyWorld, SimulationResult
from tinytroupe.agent_types import Content
from tinytroupe.ml_models import EngagementPredictor
from tinytroupe.content_generation import ContentVariantGenerator

class SimulationConfig:
    def __init__(self, name: str, persona_count: int = 10, network_type: str = "scale_free", use_linkedin_audience: bool = False, linkedin_token: str = None):
        self.name = name
        self.persona_count = persona_count
        self.network_type = network_type
        self.use_linkedin_audience = use_linkedin_audience
        self.linkedin_token = linkedin_token

class Simulation:
    def __init__(self, id: str, config: SimulationConfig, world: SocialTinyWorld, personas: List[TinyPerson], network: NetworkTopology):
        self.id = id
        self.config = config
        self.world = world
        self.personas = personas
        self.network = network
        self.status = "ready"
        self.created_at = datetime.now()
        self.last_result = None

class SimulationManager:
    """Manages simulation lifecycle and execution"""

    def __init__(self):
        self.simulations: Dict[str, Simulation] = {}
        self.predictor = EngagementPredictor()
        self.variant_generator = ContentVariantGenerator()

    def create_simulation(self, config: SimulationConfig) -> Simulation:
        from tinytroupe.factory.tiny_person_factory import TinyPersonFactory
        factory = TinyPersonFactory()
        personas = factory.generate_people(number_of_people=config.persona_count)

        from tinytroupe.network_generator import NetworkGenerator
        if config.network_type == "scale_free":
            network = NetworkGenerator.generate_scale_free_network(personas)
        else:
            network = NetworkGenerator.generate_professional_network(personas)

        world = SocialTinyWorld(config.name, network)
        for p in personas: world.add_agent(p)

        sim_id = hashlib.md5(f"{config.name}{datetime.now()}".encode()).hexdigest()
        sim = Simulation(sim_id, config, world, personas, network)
        self.simulations[sim_id] = sim
        return sim

    def run_simulation(self, sim_id: str, content_text: str) -> SimulationResult:
        sim = self.simulations[sim_id]
        sim.status = "running"
        content = Content(text=content_text, content_type="post", topics=[], length=len(content_text), tone="")

        initial_viewers = [p.name for p in sim.personas[:min(5, len(sim.personas))]]
        result = sim.world.simulate_content_spread(content, initial_viewers)

        sim.status = "completed"
        sim.last_result = result
        return result
