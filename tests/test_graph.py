"""
Unit and Correctness Tests for RoadGraph and Dijkstra's Algorithm
Phase 3 Evidence: Adjacency list representation, min-heap priority queue, path reconstruction.
"""

import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import DeliveryPoint
from core.graph import RoadGraph


class TestRoadGraphDijkstra(unittest.TestCase):
    def setUp(self):
        self.graph = RoadGraph()
        # Create a diamond graph:
        #        A (0)
        #       / \
        #   1  /   \ 4
        #     B     C
        #      \   /
        #    2  \ / 1
        #        D (3)
        self.graph.add_node(DeliveryPoint("A", "Origin", 0, 0, is_depot=True))
        self.graph.add_node(DeliveryPoint("B", "Waypoint B", 1, 1))
        self.graph.add_node(DeliveryPoint("C", "Waypoint C", 1, -1))
        self.graph.add_node(DeliveryPoint("D", "Destination", 2, 0))

        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("A", "C", 4.0)
        self.graph.add_edge("B", "D", 2.0)
        self.graph.add_edge("C", "D", 1.0)

    def test_dijkstra_shortest_path(self):
        """Verifies Dijkstra chooses A -> B -> D (cost 3.0) over A -> C -> D (cost 5.0)."""
        dists, preds = self.graph.dijkstra("A")
        self.assertEqual(dists["D"], 3.0)
        self.assertEqual(dists["B"], 1.0)
        self.assertEqual(dists["C"], 4.0)

        path_to_d = self.graph.reconstruct_path("A", "D", preds)
        self.assertEqual(path_to_d, ["A", "B", "D"])

    def test_all_pairs_matrix(self):
        """Tests that compute_all_pairs_matrix computes symmetric paths for undirected edges."""
        dist_matrix, path_matrix = self.graph.compute_all_pairs_matrix(["A", "B", "C", "D"])
        self.assertEqual(dist_matrix["A"]["D"], 3.0)
        self.assertEqual(dist_matrix["D"]["A"], 3.0)
        self.assertEqual(path_matrix["A"]["D"], ["A", "B", "D"])
        self.assertEqual(path_matrix["D"]["A"], ["D", "B", "A"])


if __name__ == "__main__":
    unittest.main()

