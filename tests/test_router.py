"""
Unit and Correctness Tests for TSP Routing Algorithms
Phase 3 Evidence: Nearest Neighbor approximation and 2-Opt local search improvement.
"""

import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Parcel, DeliveryPoint
from core.graph import RoadGraph
from core.router import RouteOptimizer


class TestTSPRouting(unittest.TestCase):
    def setUp(self):
        # Create a 4-corner square network:
        # DEPOT(0,0) --- LOC-1(10,0)
        #     |              |
        # LOC-3(0,10) -- LOC-2(10,10)
        self.graph = RoadGraph()
        self.graph.add_node(DeliveryPoint("DEPOT", "Depot", 0.0, 0.0, is_depot=True))
        self.graph.add_node(DeliveryPoint("LOC-1", "Point 1", 10.0, 0.0))
        self.graph.add_node(DeliveryPoint("LOC-2", "Point 2", 10.0, 10.0))
        self.graph.add_node(DeliveryPoint("LOC-3", "Point 3", 0.0, 10.0))

        # Explicit edges with Euclidean distances
        self.graph.add_edge("DEPOT", "LOC-1", 10.0)
        self.graph.add_edge("LOC-1", "LOC-2", 10.0)
        self.graph.add_edge("LOC-2", "LOC-3", 10.0)
        self.graph.add_edge("LOC-3", "DEPOT", 10.0)
        # Diagonals (approx 14.14)
        self.graph.add_edge("DEPOT", "LOC-2", 14.14)
        self.graph.add_edge("LOC-1", "LOC-3", 14.14)

        self.router = RouteOptimizer(self.graph)

    def test_tsp_visits_all_destinations_and_returns(self):
        """Verifies TSP starts at DEPOT, visits all required nodes, and returns to DEPOT."""
        parcels = [
            Parcel("P1", "LOC-1", "High", 2.0, 2.0, 3.0, 50.0),
            Parcel("P2", "LOC-2", "High", 2.0, 2.0, 3.0, 50.0),
            Parcel("P3", "LOC-3", "High", 2.0, 2.0, 3.0, 50.0),
        ]
        tour, total_dist, legs, stats = self.router.plan_delivery_route("DEPOT", parcels, use_2opt=True)

        self.assertEqual(tour[0], "DEPOT")
        self.assertEqual(tour[-1], "DEPOT")
        visited_set = set(tour)
        self.assertEqual(visited_set, {"DEPOT", "LOC-1", "LOC-2", "LOC-3"})
        self.assertEqual(len(tour), 5)  # DEPOT -> 3 stops -> DEPOT
        # Optimal perimeter of square is 10 + 10 + 10 + 10 = 40.0
        self.assertAlmostEqual(total_dist, 40.0, delta=0.5)

    def test_two_opt_untangling(self):
        """Verifies 2-Opt strictly reduces or maintains tour distance."""
        parcels = [
            Parcel("P1", "LOC-1", "High", 2.0, 2.0, 3.0, 50.0),
            Parcel("P2", "LOC-2", "High", 2.0, 2.0, 3.0, 50.0),
            Parcel("P3", "LOC-3", "High", 2.0, 2.0, 3.0, 50.0),
        ]
        _, _, _, stats = self.router.plan_delivery_route("DEPOT", parcels, use_2opt=True)
        self.assertLessEqual(stats["final_distance_km"], stats["nn_distance_km"])


if __name__ == "__main__":
    unittest.main()

