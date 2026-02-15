from typing import List, Set, Dict, Any, Optional
from datetime import datetime
import random
from tinytroupe.environment.tiny_world import TinyWorld
from tinytroupe.social_network import NetworkTopology, Community
from tinytroupe.agent_types import Content
from tinytroupe.agent.tiny_person import TinyPerson

class EngagementDecision:
    def __init__(self, engaged: bool, engagement_type: str = "none", comment: str = None, probability: float = 0.0):
        self.engaged = engaged
        self.engagement_type = engagement_type
        self.comment = comment
        self.probability = probability

class SimulationResult:
    def __init__(self, content: Content, start_time: datetime):
        self.content = content
        self.start_time = start_time
        self.engagements = []
        self.step_metrics = []
        self.end_time = None
        self.total_reach = 0

    def add_engagement(self, persona_id: str, engagement_type: str, step: int):
        self.engagements.append({"persona_id": persona_id, "type": engagement_type, "step": step})

    def add_step_metrics(self, step: int, viewed: int, engaged: int):
        self.step_metrics.append({"step": step, "viewed": viewed, "engaged": engaged})

    def finalize(self, end_time: datetime):
        self.end_time = end_time
        self.total_reach = self.step_metrics[-1]["viewed"] if self.step_metrics else 0

class SocialTinyWorld(TinyWorld):
    """Extended TinyWorld with social network capabilities"""

    def __init__(self, name: str, network: NetworkTopology = None, **kwargs):
        super().__init__(name, **kwargs)
        self.network = network or NetworkTopology()
        self.content_items: List[Content] = []
        self.simulation_history = []
        self.time_step = 0

    def add_content(self, content: Content) -> None:
        """Add content to the world for personas to interact with"""
        self.content_items.append(content)
        self.broadcast(f"New content available: {content.text[:100]}...")

    def simulate_content_spread(self, content: Content,
                               initial_viewers: List[str],
                               max_steps: int = 10) -> SimulationResult:
        """Simulate how content spreads through the network"""

        result = SimulationResult(content=content, start_time=datetime.now())
        viewed = set(initial_viewers)
        engaged = set()

        for step in range(max_steps):
            self.time_step = step
            new_viewers = set()

            for viewer_id in viewed - engaged:
                if viewer_id not in self.network.nodes: continue
                persona = self.network.nodes[viewer_id]
                decision = self._simulate_engagement_decision(persona, content, step)

                if decision.engaged:
                    engaged.add(viewer_id)
                    result.add_engagement(viewer_id, decision.engagement_type, step)
                    if decision.engagement_type == "share":
                        neighbors = self.network.get_neighbors(viewer_id)
                        new_viewers.update([n.name for n in neighbors])

            viewed.update(new_viewers)
            result.add_step_metrics(step, len(viewed), len(engaged))
            if not new_viewers and not any(v not in engaged for v in viewed):
                break

        result.finalize(datetime.now())
        self.simulation_history.append(result)
        return result

    def _simulate_engagement_decision(self, persona: TinyPerson,
                                     content: Content,
                                     time_step: int) -> EngagementDecision:
        prob = persona.calculate_engagement_probability(content)
        time_decay = 0.9 ** time_step
        final_prob = prob * time_decay

        engaged = random.random() < final_prob
        if engaged:
            reaction = persona.predict_reaction(content)
            return EngagementDecision(
                engaged=True,
                engagement_type=reaction.reaction_type,
                comment=reaction.comment,
                probability=final_prob
            )
        return EngagementDecision(engaged=False, probability=final_prob)
