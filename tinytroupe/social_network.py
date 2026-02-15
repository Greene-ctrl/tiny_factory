from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set, Tuple
from datetime import datetime
import numpy as np
from tinytroupe.agent.tiny_person import TinyPerson

@dataclass
class Connection:
    """Represents a connection between two personas"""
    source_id: str
    target_id: str
    strength: float = 0.5 # 0.0-1.0
    relationship_type: str = "follower" # "follower", "friend", "colleague", "family"
    interaction_frequency: float = 0.0 # interactions per week
    last_interaction: Optional[datetime] = None
    influence_score: float = 0.0 # how much target influences source
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Community:
    """Represents a cluster of closely connected personas"""
    community_id: str
    members: List[str] # persona_ids
    density: float = 0.0
    central_personas: List[str] = field(default_factory=list) # most influential in community
    shared_interests: List[str] = field(default_factory=list)
    avg_engagement_rate: float = 0.0

class NetworkTopology:
    """Represents the entire social network structure"""
    def __init__(self):
        self.nodes: Dict[str, TinyPerson] = {} # persona_id -> persona
        self.edges: List[Connection] = []
        self.adjacency_matrix: Optional[np.ndarray] = None
        self.influence_matrix: Optional[np.ndarray] = None
        self.communities: List[Community] = []

    def add_persona(self, persona: TinyPerson) -> None:
        self.nodes[persona.name] = persona

    def add_connection(self, source_id: str, target_id: str, **kwargs) -> Connection:
        conn = Connection(source_id=source_id, target_id=target_id, **kwargs)
        self.edges.append(conn)
        return conn

    def remove_connection(self, source_id: str, target_id: str) -> None:
        self.edges = [e for e in self.edges if not (e.source_id == source_id and e.target_id == target_id)]

    def get_neighbors(self, persona_id: str, depth: int = 1) -> List[TinyPerson]:
        # Simple BFS for neighbors
        neighbors = set()
        queue = [(persona_id, 0)]
        visited = {persona_id}

        while queue:
            curr_id, curr_depth = queue.pop(0)
            if curr_depth >= depth: continue

            for edge in self.edges:
                if edge.source_id == curr_id and edge.target_id not in visited:
                    neighbors.add(edge.target_id)
                    visited.add(edge.target_id)
                    queue.append((edge.target_id, curr_depth + 1))
                elif edge.target_id == curr_id and edge.source_id not in visited:
                    neighbors.add(edge.source_id)
                    visited.add(edge.source_id)
                    queue.append((edge.source_id, curr_depth + 1))

        return [self.nodes[nid] for nid in neighbors if nid in self.nodes]

    def calculate_centrality_metrics(self) -> Dict[str, float]:
        # Placeholder for real centrality (e.g. using NetworkX in analysis module)
        metrics = {name: 0.0 for name in self.nodes}
        for edge in self.edges:
            metrics[edge.source_id] += 1
            metrics[edge.target_id] += 1
        return metrics

    def detect_communities(self) -> List[Community]:
        # Placeholder
        return self.communities
