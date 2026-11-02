"""
Road Graph & Dijkstra's Shortest Path Algorithm Module
Phase 3: Route Maker and Graph Processing
Implements Adjacency List graph representation and Min-Heap Dijkstra's Algorithm
with predecessor tracking for turn-by-turn path reconstruction.
"""

import heapq
import math
import time
from typing import Dict, List, Tuple, Optional, Any
from core.models import DeliveryPoint, RoadEdge


class RoadGraph:
    """
    Weighted Directed/Undirected Graph representation of road networks.
    Uses an Adjacency List for space and time efficiency: O(V + E).
    """
    def __init__(self):
        self.nodes: Dict[str, DeliveryPoint] = {}
        self.adj: Dict[str, List[Tuple[str, float]]] = {}
        self.edges: List[RoadEdge] = []

    def add_node(self, node: DeliveryPoint):
        """Registers a delivery point or road intersection in the graph."""
        self.nodes[node.id] = node
        if node.id not in self.adj:
            self.adj[node.id] = []

    def add_edge(self, source: str, destination: str, distance: float, bidirectional: bool = True):
        """Adds a weighted road edge between two nodes."""
        if source not in self.adj:
            self.adj[source] = []
        if destination not in self.adj:
            self.adj[destination] = []

        self.adj[source].append((destination, distance))
        self.edges.append(RoadEdge(source, destination, distance, bidirectional))

        if bidirectional:
            self.adj[destination].append((source, distance))

    def get_depot(self) -> Optional[DeliveryPoint]:
        """Finds the designated Depot node."""
        for node in self.nodes.values():
            if node.is_depot:
                return node
        # Default to first node if none flagged explicitly
        return list(self.nodes.values())[0] if self.nodes else None

    def dijkstra(self, source_id: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Executes Dijkstra's algorithm from a single source node.
        Uses a Min-Heap (priority queue) yielding O((V + E) log V) time complexity.
        
        Returns:
        - distances: Mapping of node_id -> shortest path distance from source_id
        - predecessors: Mapping of node_id -> predecessor node on the shortest path
        """
        if source_id not in self.adj:
            raise ValueError(f"Source node '{source_id}' does not exist in graph.")

        distances: Dict[str, float] = {node_id: float('inf') for node_id in self.nodes}
        predecessors: Dict[str, Optional[str]] = {node_id: None for node_id in self.nodes}

        distances[source_id] = 0.0

        # Min-heap stores tuples of (current_distance, node_id)
        pq: List[Tuple[float, str]] = [(0.0, source_id)]

        visited = set()

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u in visited:
                continue
            visited.add(u)

            # Relaxation step
            for neighbor, weight in self.adj.get(u, []):
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = u
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances, predecessors

    def reconstruct_path(self, source_id: str, target_id: str, predecessors: Dict[str, Optional[str]]) -> List[str]:
        """
        Reconstructs the sequence of nodes along the shortest path from source to target.
        """
        if source_id == target_id:
            return [source_id]

        path = []
        curr = target_id

        while curr is not None:
            path.append(curr)
            if curr == source_id:
                break
            curr = predecessors.get(curr)

        path.reverse()
        if not path or path[0] != source_id:
            return []  # Target unreachable
        return path

    def compute_all_pairs_matrix(
        self,
        required_nodes: List[str]
    ) -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, List[str]]]]:
        """
        Computes the shortest path distance matrix and path dictionary between
        all pairs of required nodes (Depot + Delivery locations).
        
        Returns:
        - dist_matrix: dist_matrix[u][v] = shortest distance from u to v
        - path_matrix: path_matrix[u][v] = full turn-by-turn road node path from u to v
        """
        dist_matrix: Dict[str, Dict[str, float]] = {u: {} for u in required_nodes}
        path_matrix: Dict[str, Dict[str, List[str]]] = {u: {} for u in required_nodes}

        for u in required_nodes:
            dists, preds = self.dijkstra(u)
            for v in required_nodes:
                dist_matrix[u][v] = round(dists.get(v, float('inf')), 3)
                path_matrix[u][v] = self.reconstruct_path(u, v, preds)

        return dist_matrix, path_matrix

    @classmethod
    def create_from_nodes_and_edges(
        cls,
        nodes_data: List[Dict[str, Any]],
        edges_data: Optional[List[Dict[str, Any]]] = None
    ) -> "RoadGraph":
        """
        Constructs a RoadGraph from raw dictionaries.
        If edges are not supplied, creates a Delaunay-like or complete Euclidean mesh
        with realistic road network distances.
        """
        graph = cls()

        for nd in nodes_data:
            node = DeliveryPoint.from_dict(nd)
            graph.add_node(node)

        if edges_data:
            for ed in edges_data:
                graph.add_edge(
                    source=ed["source"],
                    destination=ed["destination"],
                    distance=float(ed["distance"]),
                    bidirectional=ed.get("bidirectional", True)
                )
        else:
            # Generate road network edges using Euclidean distances + 10-25% road tortuosity
            node_ids = list(graph.nodes.keys())
            for i in range(len(node_ids)):
                u_id = node_ids[i]
                u_node = graph.nodes[u_id]
                for j in range(i + 1, len(node_ids)):
                    v_id = node_ids[j]
                    v_node = graph.nodes[v_id]

                    dx = u_node.x - v_node.x
                    dy = u_node.y - v_node.y
                    euclidean = math.sqrt(dx * dx + dy * dy)

                    # Connect all nodes within a reasonable proximity, or guarantee connected graph
                    road_dist = round(euclidean * 1.15, 2)
                    graph.add_edge(u_id, v_id, road_dist, bidirectional=True)

        return graph

