from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass
from tinytroupe.content_generation import ContentVariant
from tinytroupe.agent.tiny_person import TinyPerson
from tinytroupe.social_network import NetworkTopology
from tinytroupe.ml_models import EngagementPredictor

@dataclass
class RankedVariant:
    variant: ContentVariant
    score: float
    predicted_engagement_count: int

class VariantOptimizer:
    """Optimize and rank content variants"""

    def __init__(self, predictor: EngagementPredictor):
        self.predictor = predictor

    def rank_variants(self, variants: List[ContentVariant],
                      target_personas: List[TinyPerson],
                      network: NetworkTopology) -> List[RankedVariant]:
        """Rank variants by predicted performance"""
        ranked = []
        for variant in variants:
            probs = []
            from tinytroupe.agent_types import Content
            content_obj = Content(text=variant.text, content_type="article", topics=[], length=len(variant.text), tone="")

            for persona in target_personas:
                prob = self.predictor.predict(persona, content_obj, network)
                probs.append(prob)

            avg_prob = np.mean(probs) if probs else 0.0
            ranked.append(RankedVariant(
                variant=variant,
                score=avg_prob,
                predicted_engagement_count=int(sum(probs))
            ))

        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked
