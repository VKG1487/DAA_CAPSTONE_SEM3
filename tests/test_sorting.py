"""
Unit and Correctness Tests for Sorting Algorithms
Phase 2 Evidence: MergeSort, QuickSort, and Prioritization Key correctness.
"""

import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Parcel
from core.sorting import MergeSort, QuickSort, get_sort_key_fn


class TestSortingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.sample_parcels = [
            Parcel("P1", "LOC-A", "Low", deadline_hours=8.0, weight=4.0, volume=5.0, value=10.0),
            Parcel("P2", "LOC-B", "Critical", deadline_hours=1.0, weight=2.0, volume=3.0, value=50.0),
            Parcel("P3", "LOC-C", "High", deadline_hours=2.5, weight=3.0, volume=4.0, value=30.0),
            Parcel("P4", "LOC-D", "Medium", deadline_hours=4.0, weight=5.0, volume=6.0, value=20.0),
        ]

    def test_mergesort_by_deadline(self):
        """Tests that MergeSort orders parcels by earliest deadline first."""
        ms = MergeSort()
        key_fn = get_sort_key_fn("deadline")
        sorted_p = ms.sort(self.sample_parcels, key_fn)

        deadlines = [p.deadline_hours for p in sorted_p]
        self.assertEqual(deadlines, sorted(deadlines))
        self.assertEqual(sorted_p[0].id, "P2")  # 1.0 hour
        self.assertEqual(sorted_p[-1].id, "P1") # 8.0 hours

    def test_quicksort_by_priority(self):
        """Tests that QuickSort orders parcels by highest priority first."""
        qs = QuickSort()
        key_fn = get_sort_key_fn("priority")
        sorted_p = qs.sort(self.sample_parcels, key_fn)

        priorities = [p.priority for p in sorted_p]
        self.assertEqual(priorities[0], "Critical")
        self.assertEqual(priorities[1], "High")
        self.assertEqual(priorities[2], "Medium")
        self.assertEqual(priorities[3], "Low")

    def test_mergesort_quicksort_agreement(self):
        """Verifies MergeSort and QuickSort produce identical sorting on composite score."""
        key_fn = get_sort_key_fn("composite")
        ms_res = MergeSort().sort(self.sample_parcels, key_fn)
        qs_res = QuickSort().sort(self.sample_parcels, key_fn)

        ms_ids = [p.id for p in ms_res]
        qs_ids = [p.id for p in qs_res]
        self.assertEqual(ms_ids, qs_ids)

    def test_empty_and_single_item(self):
        """Boundary condition testing on edge cases."""
        ms = MergeSort()
        qs = QuickSort()
        key_fn = get_sort_key_fn("composite")

        self.assertEqual(ms.sort([], key_fn), [])
        self.assertEqual(qs.sort([], key_fn), [])
        self.assertEqual(len(ms.sort([self.sample_parcels[0]], key_fn)), 1)
        self.assertEqual(len(qs.sort([self.sample_parcels[0]], key_fn)), 1)


if __name__ == "__main__":
    unittest.main()

