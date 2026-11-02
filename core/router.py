"""
TSP Delivery Route Optimizer Module
Phase 3: Route Maker and Graph Processing
Implements Nearest Neighbor TSP Approximation and 2-Opt Local Search Improvement.
"""

import time
from typing import List, Dict, Tuple, Any
from core.graph import RoadGraph
from core.models import Parcel, DeliveryTrip


class RouteOptimizer:
    """
    Solves the Traveling Salesperson Problem (TSP) over delivery nodes
    using Nearest Neighbor Greedy Heuristic and 2-Opt local search.
    """
    def __init__(self, graph: RoadGraph):
        self.graph = graph

    def plan_delivery_route(
        self,
        depot_id: str,
        selected_parcels: List[Parcel],
        use_2opt: bool = True
    ) -> Tuple[List[str], float, List[Dict[str, Any]], Dict[str, Any]]:
        """
        Generates an ordered delivery route visiting all destinations of the selected parcels
        and returning to the depot.
        
        Returns:
        - final_tour: Ordered sequence of visited customer nodes e.g. ["DEPOT", "LOC-1", "LOC-2", "DEPOT"]
        - total_distance: Total road distance in km
        - detailed_legs: Detailed breakdown of each leg with turn-by-turn paths and parcels
        - stats: Runtime and algorithmic comparison metrics
        """
        t0 = time.perf_counter()

        # Identify unique delivery destinations among selected parcels
        destination_nodes = sorted(list(set(p.destination_id for p in selected_parcels)))

        # Remove depot if it was accidentally listed as a destination
        destination_nodes = [node for node in destination_nodes if node != depot_id]

        if not destination_nodes:
            # Nothing to deliver
            return [depot_id], 0.0, [], {"runtime_ms": 0.0, "nn_distance": 0.0, "opt2_distance": 0.0}

        # All nodes involved in TSP: Depot + all unique destinations
        required_nodes = [depot_id] + destination_nodes
        dist_matrix, path_matrix = self.graph.compute_all_pairs_matrix(required_nodes)

        # 1. Nearest Neighbor Heuristic
        t_nn_start = time.perf_counter()
        nn_tour = self._nearest_neighbor(depot_id, destination_nodes, dist_matrix)
        nn_distance = self._calculate_tour_distance(nn_tour, dist_matrix)
        t_nn = (time.perf_counter() - t_nn_start) * 1000

        # 2. 2-Opt Local Search Improvement
        final_tour = nn_tour
        opt2_distance = nn_distance
        opt2_iterations = 0
        t_2opt = 0.0

        if use_2opt and len(destination_nodes) >= 3:
            t_opt_start = time.perf_counter()
            final_tour, opt2_distance, opt2_iterations = self._two_opt(nn_tour, dist_matrix)
            t_2opt = (time.perf_counter() - t_opt_start) * 1000

        total_runtime_ms = (time.perf_counter() - t0) * 1000

        # 3. Build Detailed Leg Breakdown
        detailed_legs = []
        parcels_by_dest: Dict[str, List[Parcel]] = {}
        for p in selected_parcels:
            parcels_by_dest.setdefault(p.destination_id, []).append(p)

        for i in range(len(final_tour) - 1):
            u = final_tour[i]
            v = final_tour[i + 1]
            leg_dist = dist_matrix[u][v]
            leg_road_path = path_matrix.get(u, {}).get(v, [u, v])
            delivered = parcels_by_dest.get(v, []) if v != depot_id else []

            detailed_legs.append({
                "leg_number": i + 1,
                "from_node": u,
                "to_node": v,
                "from_name": self.graph.nodes[u].name if u in self.graph.nodes else u,
                "to_name": self.graph.nodes[v].name if v in self.graph.nodes else v,
                "distance_km": round(leg_dist, 2),
                "road_path": leg_road_path,
                "parcels_delivered": [p.id for p in delivered],
                "delivered_count": len(delivered)
            })

        stats = {
            "nn_distance_km": round(nn_distance, 2),
            "final_distance_km": round(opt2_distance, 2),
            "distance_saved_km": round(max(0.0, nn_distance - opt2_distance), 2),
            "improvement_pct": round(((nn_distance - opt2_distance) / max(nn_distance, 1e-6)) * 100, 2) if nn_distance > opt2_distance else 0.0,
            "nn_runtime_ms": round(t_nn, 4),
            "two_opt_runtime_ms": round(t_2opt, 4),
            "two_opt_iterations": opt2_iterations,
            "total_routing_ms": round(total_runtime_ms, 4)
        }

        return final_tour, opt2_distance, detailed_legs, stats

    def _nearest_neighbor(
        self,
        depot_id: str,
        destinations: List[str],
        dist_matrix: Dict[str, Dict[str, float]]
    ) -> List[str]:
        """
        Greedy Nearest Neighbor: O(K^2) time complexity.
        Always moves to the closest unvisited destination.
        """
        unvisited = set(destinations)
        tour = [depot_id]
        curr = depot_id

        while unvisited:
            next_node = min(unvisited, key=lambda node: dist_matrix[curr].get(node, float('inf')))
            tour.append(next_node)
            unvisited.remove(next_node)
            curr = next_node

        tour.append(depot_id)  # Return to depot
        return tour

    def _two_opt(
        self,
        tour: List[str],
        dist_matrix: Dict[str, Dict[str, float]],
        max_iterations: int = 500
    ) -> Tuple[List[str], float, int]:
        """
        2-Opt heuristic to iteratively untangle crossed paths.
        Systematically inverts sub-sequences when it yields a shorter overall cycle.
        """
        best_tour = list(tour)
        best_dist = self._calculate_tour_distance(best_tour, dist_matrix)
        improved = True
        iterations = 0

        n = len(best_tour)

        while improved and iterations < max_iterations:
            improved = False
            iterations += 1

            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    # Current edges: (i-1 -> i) and (j -> j+1)
                    # Candidate edges: (i-1 -> j) and (i -> j+1)
                    u1, v1 = best_tour[i - 1], best_tour[i]
                    u2, v2 = best_tour[j], best_tour[j + 1]

                    curr_cost = dist_matrix[u1][v1] + dist_matrix[u2][v2]
                    new_cost = dist_matrix[u1][u2] + dist_matrix[v1][v2]

                    if new_cost < curr_cost - 1e-4:
                        # Reverse tour segment from i to j
                        best_tour[i:j + 1] = reversed(best_tour[i:j + 1])
                        best_dist = self._calculate_tour_distance(best_tour, dist_matrix)
                        improved = True
                        break
                if improved:
                    break

        return best_tour, round(best_dist, 2), iterations

    def _calculate_tour_distance(
        self,
        tour: List[str],
        dist_matrix: Dict[str, Dict[str, float]]
    ) -> float:
        """Calculates total closed tour distance."""
        tot = 0.0
        for i in range(len(tour) - 1):
            tot += dist_matrix[tour[i]][tour[i + 1]]
        return round(tot, 2)
