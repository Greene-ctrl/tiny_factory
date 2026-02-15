from typing import List, Dict, Any
import random
from dataclasses import dataclass
from tinytroupe.agent.tiny_person import TinyPerson
from tinytroupe.agent_types import Content

@dataclass
class ContentVariant:
    text: str
    strategy: str
    parameters: Dict[str, Any]
    original_content: str

class ContentVariantGenerator:
    """Generate multiple variants of input content"""

    def generate_variants(self, original_content: str, num_variants: int = 10,
                         target_personas: List[TinyPerson] = None) -> List[ContentVariant]:
        """Generate diverse variants of content"""
        variants = []
        strategies = ["tone", "length", "format", "persona_targeted", "angle"]

        for i in range(num_variants):
            strategy = random.choice(strategies)
            # Placeholder for real LLM-based generation
            variant_text = f"[{strategy.upper()} variant {i}] {original_content[:50]}..."

            variants.append(ContentVariant(
                text=variant_text,
                strategy=strategy,
                parameters={"index": i},
                original_content=original_content
            ))

        return variants
