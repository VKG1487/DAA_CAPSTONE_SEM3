"""
Parcel Sorting Algorithms Module
Phase 2: Package Prioritization and Box Filling
Implements MergeSort and QuickSort from scratch, with configurable multi-criteria keys.
"""

import time
from typing import List, Callable, Tuple, Any
from core.models import Parcel


def get_sort_key_fn(criterion: str) -> Callable[[Parcel], Any]:
    """
    Returns a key function for sorting parcels.
    Depending on the criterion, tuples or values are returned such that
    smaller values come first in standard ascending sort.
    """
    if criterion == "deadline":
        # Earliest deadline first (ascending), secondary by priority descending
        return lambda p: (p.deadline_hours, -p.priority_level, -p.value)
    elif criterion == "priority":
        # Highest priority first (descending), secondary by deadline ascending
        return lambda p: (-p.priority_level, p.deadline_hours, -p.value)
    elif criterion == "composite":
        # Highest composite score first (descending)
        return lambda p: -p.composite_score
    elif criterion == "value_density":
        # Highest value per kg first
        return lambda p: -(p.value / max(p.weight, 0.1))
    elif criterion == "weight":
        # Lightest first
        return lambda p: p.weight
    else:
        # Default: composite score
        return lambda p: -p.composite_score


class MergeSort:
    """
    MergeSort implementation (Divide and Conquer, Stable, O(N log N)).
    Tracks number of comparisons for algorithmic analysis.
    """
    def __init__(self):
        self.comparisons = 0

    def sort(self, items: List[Parcel], key_fn: Callable[[Parcel], Any]) -> List[Parcel]:
        self.comparisons = 0
        arr = list(items)
        return self._merge_sort(arr, key_fn)

    def _merge_sort(self, arr: List[Parcel], key_fn: Callable[[Parcel], Any]) -> List[Parcel]:
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid], key_fn)
        right = self._merge_sort(arr[mid:], key_fn)
        return self._merge(left, right, key_fn)

    def _merge(self, left: List[Parcel], right: List[Parcel], key_fn: Callable[[Parcel], Any]) -> List[Parcel]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            self.comparisons += 1
            if key_fn(left[i]) <= key_fn(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


class QuickSort:
    """
    QuickSort implementation with median-of-three pivot selection.
    Tracks number of comparisons for algorithmic analysis.
    Average O(N log N), worst-case O(N^2).
    """
    def __init__(self):
        self.comparisons = 0

    def sort(self, items: List[Parcel], key_fn: Callable[[Parcel], Any]) -> List[Parcel]:
        self.comparisons = 0
        arr = list(items)
        if len(arr) > 1:
            self._quick_sort(arr, 0, len(arr) - 1, key_fn)
        return arr

    def _quick_sort(self, arr: List[Parcel], low: int, high: int, key_fn: Callable[[Parcel], Any]):
        if low < high:
            pivot_idx = self._partition(arr, low, high, key_fn)
            self._quick_sort(arr, low, pivot_idx - 1, key_fn)
            self._quick_sort(arr, pivot_idx + 1, high, key_fn)

    def _median_of_three(self, arr: List[Parcel], low: int, high: int, key_fn: Callable[[Parcel], Any]) -> int:
        mid = (low + high) // 2
        a = key_fn(arr[low])
        b = key_fn(arr[mid])
        c = key_fn(arr[high])

        # Find median among low, mid, high
        self.comparisons += 2
        if (a <= b <= c) or (c <= b <= a):
            return mid
        elif (b <= a <= c) or (c <= a <= b):
            return low
        else:
            return high

    def _partition(self, arr: List[Parcel], low: int, high: int, key_fn: Callable[[Parcel], Any]) -> int:
        pivot_idx = self._median_of_three(arr, low, high, key_fn)
        # Move pivot to end
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        pivot_val = key_fn(arr[high])

        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            if key_fn(arr[j]) <= pivot_val:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


def compare_sorting_algorithms(
    parcels: List[Parcel],
    criterion: str = "composite"
) -> Tuple[List[Parcel], dict]:
    """
    Executes MergeSort, QuickSort, and Python's built-in TimSort.
    Returns the sorted parcel list and benchmarking performance statistics.
    """
    key_fn = get_sort_key_fn(criterion)

    # 1. MergeSort
    ms = MergeSort()
    t0 = time.perf_counter()
    ms_result = ms.sort(parcels, key_fn)
    ms_time = (time.perf_counter() - t0) * 1000  # ms

    # 2. QuickSort
    qs = QuickSort()
    t0 = time.perf_counter()
    qs_result = qs.sort(parcels, key_fn)
    qs_time = (time.perf_counter() - t0) * 1000  # ms

    # 3. TimSort (Python standard sort)
    t0 = time.perf_counter()
    ts_result = sorted(parcels, key=key_fn)
    ts_time = (time.perf_counter() - t0) * 1000  # ms

    stats = {
        "mergesort": {
            "time_ms": round(ms_time, 4),
            "comparisons": ms.comparisons,
            "algorithm": "MergeSort (O(N log N))",
            "stability": "Stable"
        },
        "quicksort": {
            "time_ms": round(qs_time, 4),
            "comparisons": qs.comparisons,
            "algorithm": "QuickSort (Median-of-3)",
            "stability": "Unstable"
        },
        "timsort": {
            "time_ms": round(ts_time, 4),
            "comparisons": "N/A (C-level)",
            "algorithm": "TimSort (Hybrid)",
            "stability": "Stable"
        }
    }

    # Best choice: MergeSort provides guaranteed O(N log N) stability for tie-breaking
    return ms_result, stats

