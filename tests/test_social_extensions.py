import pytest
from tinytroupe.agent import TinyPerson
from tinytroupe.agent.social_types import Content

def test_tiny_person_social_extension():
    person = TinyPerson("Alice")
    assert hasattr(person, "social_connections")
    assert hasattr(person, "engagement_patterns")
    assert hasattr(person, "calculate_engagement_probability")

    content = Content(text="Hello world", topics=["tech"], format="text")
    prob = person.calculate_engagement_probability(content)
    assert isinstance(prob, float)

    reaction = person.predict_reaction(content)
    assert reaction.probability == prob

def test_simulation_manager():
    from tinytroupe.simulation_manager import SimulationManager, SimulationConfig
    manager = SimulationManager()
    config = SimulationConfig(name="Test Sim", persona_count=2)
    sim = manager.create_simulation(config)

    assert sim.id is not None
    assert len(sim.personas) == 2
    assert sim.world is not None

    content = Content(text="Social media post")
    result = manager.run_simulation(sim.id, content)
    assert result.total_reach >= 0
