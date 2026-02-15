from typing import List, Set, Dict, Any
import random
from dataclasses import dataclass
from tinytroupe.social_network import NetworkTopology
from tinytroupe.agent_types import Content

@dataclass
class PropagationResult:
    activated_personas: Set[str]
    activation_times: Dict[str, int]
    total_reach: int
    cascade_depth: int
    engagement_by_time: List[int]

class InfluencePropagator:
    def __init__(self, network: NetworkTopology, model: str = "cascade"):
        self.network = network
        self.model = model
        self.max_steps = 10

    def propagate(self, seed_personas: List[str], content: Content) -> PropagationResult:
        """Main propagation simulation"""
        activated = set(seed_personas)
        activation_times = {pid: 0 for pid in seed_personas}
        engagement_by_time = [len(seed_personas)]

        for time_step in range(1, self.max_steps + 1):
            newly_activated = self._propagate_step(activated, content, time_step)
            if not newly_activated:
                break

            for pid in newly_activated:
                activation_times[pid] = time_step
            activated.update(newly_activated)
            engagement_by_time.append(len(newly_activated))

        return PropagationResult(
            activated_personas=activated,
            activation_times=activation_times,
            total_reach=len(activated),
            cascade_depth=max(activation_times.values()) if activation_times else 0,
            engagement_by_time=engagement_by_time
        )

    def _propagate_step(self, activated: Set[str], content: Content, time: int) -> Set[str]:
        """Single step of propagation"""
        newly_activated = set()

        if self.model == "cascade":
            for active_id in activated:
                # Find neighbors of active node
                neighbors = self.network.get_neighbors(active_id)
                for neighbor in neighbors:
                    if neighbor.name not in activated and neighbor.name not in newly_activated:
                        # Probabilistic activation
                        prob = 0.1 # Base propagation probability
                        if random.random() < prob:
                            newly_activated.add(neighbor.name)

        elif self.model == "threshold":
            for name, persona in self.network.nodes.items():
                if name not in activated:
                    neighbors = self.network.get_neighbors(name)
                    active_neighbors = [n for n in neighbors if n.name in activated]
                    if neighbors:
                        influence = len(active_neighbors) / len(neighbors)
                        threshold = 0.5 # Default threshold
                        if influence >= threshold:
                            newly_activated.add(name)

        return newly_activated

    def calculate_influence_score(self, persona_id: str) -> float:
        """Calculate overall influence of a persona"""
        neighbors = self.network.get_neighbors(persona_id)
        # Combine degree centrality and reach
        return len(neighbors) / max(len(self.network.nodes), 1)
