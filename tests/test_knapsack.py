"""
Unit and Correctness Tests for 0/1 Knapsack Dynamic Programming
Phase 2 Evidence: Mathematical correctness of DP recurrence, table size, and backtracking.
"""

import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Parcel
from core.knapsack import solve_01_knapsack_dp, solve_fractional_knapsack_greedy


class TestKnapsackDP(unittest.TestCase):
    def test_classic_textbook_01_knapsack(self):
        """
        Classic textbook instance:
        Items:
          1: weight = 2, value = 3
          2: weight = 3, value = 4
          3: weight = 4, value = 5
          4: weight = 5, value = 6
        Capacity = 5
        Optimal subset: Items 1 and 2 (weight = 5, value = 7)
        """
        parcels = [
            Parcel("T1", "LOC-A", "High", 3.0, weight=2.0, volume=2.0, value=3.0),
            Parcel("T2", "LOC-B", "High", 3.0, weight=3.0, volume=3.0, value=4.0),
            Parcel("T3", "LOC-C", "High", 3.0, weight=4.0, volume=4.0, value=5.0),
            Parcel("T4", "LOC-D", "High", 3.0, weight=5.0, volume=5.0, value=6.0),
        ]

        result = solve_01_knapsack_dp(
            parcels=parcels,
            weight_capacity=5.0,
            value_mode="monetary",
            scale_factor=1.0
        )

        self.assertEqual(result.total_value, 7.0)
        self.assertEqual(result.total_weight, 5.0)
        selected_ids = {p.id for p in result.selected_parcels}
        self.assertEqual(selected_ids, {"T1", "T2"})

    def test_capacity_exceeded_items_rejected(self):
        """Verify that items strictly exceeding capacity are properly deferred."""
        parcels = [
            Parcel("HEAVY", "LOC-A", "Critical", 1.0, weight=20.0, volume=10.0, value=100.0),
            Parcel("LIGHT", "LOC-B", "Low", 5.0, weight=5.0, volume=5.0, value=25.0),
        ]
        result = solve_01_knapsack_dp(parcels, weight_capacity=10.0, value_mode="monetary")
        self.assertEqual(len(result.selected_parcels), 1)
        self.assertEqual(result.selected_parcels[0].id, "LIGHT")
        self.assertEqual(len(result.unselected_parcels), 1)
        self.assertEqual(result.unselected_parcels[0].id, "HEAVY")

    def test_greedy_fractional_upper_bound(self):
        """Verify that the continuous Fractional Knapsack value >= 0/1 integer solution."""
        parcels = [
            Parcel("P1", "LOC-A", "High", 2.0, weight=10.0, volume=10.0, value=60.0),
            Parcel("P2", "LOC-B", "High", 2.0, weight=20.0, volume=20.0, value=100.0),
            Parcel("P3", "LOC-C", "High", 2.0, weight=30.0, volume=30.0, value=120.0),
        ]
        cap = 50.0
        dp_res = solve_01_knapsack_dp(parcels, weight_capacity=cap, value_mode="monetary")
        frac_res = solve_fractional_knapsack_greedy(parcels, weight_capacity=cap, value_mode="monetary")

        # Fractional value must be >= 0/1 integer value
        self.assertGreaterEqual(frac_res["upper_bound_value"], dp_res.total_value)


if __name__ == "__main__":
    unittest.main()

