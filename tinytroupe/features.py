from typing import Dict, List, Any
import numpy as np
from datetime import datetime
from tinytroupe.agent.tiny_person import TinyPerson
from tinytroupe.agent_types import Content
from tinytroupe.social_network import NetworkTopology

class ContentFeatureExtractor:
    def extract(self, content: Content) -> Dict[str, float]:
        """Extract all content features"""
        return {
            "word_count": len(content.text.split()) / 500.0, # Normalized
            "has_image": 1.0 if content.images else 0.0,
            "has_video": 1.0 if content.video_url else 0.0,
            "num_hashtags": len(content.hashtags) / 10.0,
            "sentiment_score": 0.5, # Placeholder for VADER/Transformers
            "hour_of_day": content.timestamp.hour / 24.0,
            "is_weekend": 1.0 if content.timestamp.weekday() >= 5 else 0.0,
        }

class PersonaFeatureExtractor:
    def extract(self, persona: TinyPerson) -> Dict[str, float]:
        """Extract persona features"""
        traits = persona.get("behavioral_traits") or {}
        return {
            "age": float(persona.get("age") or 30) / 100.0,
            "num_connections": len(persona.social_connections) / 100.0,
            "authority": persona.influence_metrics.authority,
            "openness": traits.get("openness_to_new_ideas", 0.5),
            "extraversion": traits.get("extraversion", 0.5),
            "engagement_rate": persona.influence_metrics.engagement_rate,
        }

class InteractionFeatureExtractor:
    def extract(self, persona: TinyPerson, content: Content, network: NetworkTopology) -> Dict[str, float]:
        """Extract features from persona-content interaction context"""
        # Placeholder for complex context features
        return {
            "topic_alignment": persona.get_content_affinity(content),
            "author_connection": 1.0 if content.author_name in persona.social_connections else 0.0,
        }

class FeatureExtractor:
    def __init__(self):
        self.content_extractor = ContentFeatureExtractor()
        self.persona_extractor = PersonaFeatureExtractor()
        self.interaction_extractor = InteractionFeatureExtractor()

    def extract_all(self, persona: TinyPerson, content: Content, network: NetworkTopology) -> np.ndarray:
        c_feats = self.content_extractor.extract(content)
        p_feats = self.persona_extractor.extract(persona)
        i_feats = self.interaction_extractor.extract(persona, content, network)

        combined = {**c_feats, **p_feats, **i_feats}
        return np.array(list(combined.values()))
