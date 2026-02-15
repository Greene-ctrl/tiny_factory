import random
from typing import List, Dict
from tinytroupe.social_network import NetworkTopology, Community
from tinytroupe.agent.tiny_person import TinyPerson

class NetworkGenerator:
    """
    Implements realistic network topologies.
    """

    @staticmethod
    def generate_scale_free_network(personas: List[TinyPerson], m: int = 2) -> NetworkTopology:
        """
        Barabási-Albert model for scale-free networks.
        """
        topology = NetworkTopology()
        for p in personas:
            topology.add_persona(p)

        names = [p.name for p in personas]
        if len(names) <= m:
            return topology

        # Initial complete graph of m nodes
        for i in range(m):
            for j in range(i + 1, m):
                topology.add_connection(names[i], names[j])

        # Add remaining nodes with preferential attachment
        for i in range(m, len(names)):
            targets = set()
            existing_nodes = names[:i]
            # Simple preferential attachment based on degree
            while len(targets) < m:
                # Degree of each node
                degrees = {name: 0 for name in existing_nodes}
                for edge in topology.edges:
                    if edge.source_id in degrees: degrees[edge.source_id] += 1
                    if edge.target_id in degrees: degrees[edge.target_id] += 1

                total_degree = sum(degrees.values())
                if total_degree == 0:
                    target = random.choice(existing_nodes)
                else:
                    probs = [degrees[name] / total_degree for name in existing_nodes]
                    target = random.choices(existing_nodes, weights=probs)[0]
                targets.add(target)

            for target in targets:
                topology.add_connection(names[i], target)

        return topology

    @staticmethod
    def generate_small_world_network(personas: List[TinyPerson], k: int = 4, p: float = 0.1) -> NetworkTopology:
        """
        Watts-Strogatz model for small-world networks.
        """
        topology = NetworkTopology()
        for persona in personas:
            topology.add_persona(persona)

        names = [p.name for p in personas]
        n = len(names)

        # Regular ring lattice
        for i in range(n):
            for j in range(1, k // 2 + 1):
                neighbor = names[(i + j) % n]
                topology.add_connection(names[i], neighbor)

        # Rewiring
        for i in range(n):
            for j in range(1, k // 2 + 1):
                if random.random() < p:
                    # Remove old connection and add a random one
                    old_neighbor = names[(i + j) % n]
                    topology.remove_connection(names[i], old_neighbor)
                    new_neighbor = random.choice(names)
                    while new_neighbor == names[i] or any(e.source_id == names[i] and e.target_id == new_neighbor for e in topology.edges):
                         new_neighbor = random.choice(names)
                    topology.add_connection(names[i], new_neighbor)

        return topology

    @staticmethod
    def generate_professional_network(personas: List[TinyPerson]) -> NetworkTopology:
        """
        LinkedIn-style network based on professional attributes.
        """
        topology = NetworkTopology()
        for p in personas:
            topology.add_persona(p)

        for i, p1 in enumerate(personas):
            for j in range(i + 1, len(personas)):
                p2 = personas[j]
                # Probabilistic connection based on similarity
                prob = 0.05
                if p1.get("occupation") == p2.get("occupation"): prob += 0.2
                if p1.get("residence") == p2.get("residence"): prob += 0.1

                if random.random() < prob:
                    topology.add_connection(p1.name, p2.name, relationship_type="colleague")

        return topology
