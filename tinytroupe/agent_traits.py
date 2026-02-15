from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import random
import json
from tinytroupe.agent_types import Action
from tinytroupe import openai_utils

@dataclass
class TraitProfile:
    openness_to_new_ideas: float = 0.5
    conscientiousness: float = 0.5
    extraversion: float = 0.5
    agreeableness: float = 0.5
    controversiality_tolerance: float = 0.5
    information_seeking_behavior: float = 0.5
    visual_content_preference: float = 0.5

    def to_dict(self):
        return {
            "openness_to_new_ideas": self.openness_to_new_ideas,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "agreeableness": self.agreeableness,
            "controversiality_tolerance": self.controversiality_tolerance,
            "information_seeking_behavior": self.information_seeking_behavior,
            "visual_content_preference": self.visual_content_preference
        }

class TraitBasedBehaviorModel:
    """
    Handles behavior modeling based on granular personality traits.
    """

    def compute_action_probability(self, persona, action: Action) -> float:
        """
        Computes the probability of an action based on persona traits.
        """
        traits = persona.get("behavioral_traits") or TraitProfile().to_dict()
        base_prob = 0.5

        # Influence of traits on common actions
        if action.type == "SHARE":
            base_prob = self.apply_trait_modifiers(base_prob, {"extraversion": traits.get("extraversion", 0.5)})
        elif action.type == "COMMENT":
            base_prob = self.apply_trait_modifiers(base_prob, {"agreeableness": traits.get("agreeableness", 0.5)})

        return base_prob

    def apply_trait_modifiers(self, base_probability: float, traits: Dict[str, float]) -> float:
        """
        Applies trait-based modifiers to a base probability.
        """
        modified_prob = base_probability
        for trait, value in traits.items():
            # Simplistic linear modification for now
            modified_prob *= (0.5 + value)

        return min(max(modified_prob, 0.0), 1.0)

    @staticmethod
    def generate_trait_profile_from_description(description: str) -> TraitProfile:
        """
        Uses LLM to infer traits from a persona description.
        """
        # Placeholder for LLM-based trait extraction
        # In a real implementation, this would call openai_utils.client().send_message(...)

        # Example logic for synthetic variation
        return TraitProfile(
            openness_to_new_ideas=random.uniform(0.1, 0.9),
            conscientiousness=random.uniform(0.1, 0.9),
            extraversion=random.uniform(0.1, 0.9),
            agreeableness=random.uniform(0.1, 0.9),
            controversiality_tolerance=random.uniform(0.1, 0.9),
            information_seeking_behavior=random.uniform(0.1, 0.9),
            visual_content_preference=random.uniform(0.1, 0.9)
        )
