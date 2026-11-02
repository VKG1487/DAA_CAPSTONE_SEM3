"""
Dynamic Programming Knapsack & Box Filling Module
Phase 2: Package Prioritization and Box Filling
Implements 0/1 Knapsack DP with full DP matrix, backtracking reconstruction,
volume validation, and comparison with Greedy Fractional Knapsack.
"""

import time
from typing import List, Tuple, Dict, Any, Optional
import pandas as pd
from core.models import Parcel


class KnapsackResult:
    """Encapsulates the output of the 0/1 Knapsack DP algorithm."""
    def __init__(
        self,
        selected_parcels: List[Parcel],
        unselected_parcels: List[Parcel],
        total_weight: float,
        total_volume: float,
        total_value: float,
        weight_capacity: float,
        volume_capacity: float,
        dp_table: List[List[float]],
        weight_labels: List[int],
        item_labels: List[str],
        execution_time_ms: float,
        scale_factor: float
    ):
        self.selected_parcels = selected_parcels
        self.unselected_parcels = unselected_parcels
        self.total_weight = round(total_weight, 2)
        self.total_volume = round(total_volume, 2)
        self.total_value = round(total_value, 2)
        self.weight_capacity = weight_capacity
        self.volume_capacity = volume_capacity
        self.dp_table = dp_table
        self.weight_labels = weight_labels
        self.item_labels = item_labels
        self.execution_time_ms = round(execution_time_ms, 4)
        self.scale_factor = scale_factor

    @property
    def weight_utilization_pct(self) -> float:
        if self.weight_capacity <= 0:
            return 0.0
        return round((self.total_weight / self.weight_capacity) * 100.0, 1)

    @property
    def volume_utilization_pct(self) -> float:
        if self.volume_capacity <= 0:
            return 0.0
        return round((self.total_volume / self.volume_capacity) * 100.0, 1)

    def get_dp_dataframe(self, max_cols: int = 25) -> pd.DataFrame:
        """
        Converts the DP matrix into a clean, human-readable pandas DataFrame.
        Caps columns if weight table is very wide for clear UI rendering.
        """
        cols = [f"{w / self.scale_factor:.1f}kg" for w in self.weight_labels]
        df = pd.DataFrame(self.dp_table, index=self.item_labels, columns=cols)
        if len(cols) > max_cols:
            # Sample columns evenly plus the last column
            step = max(1, len(cols) // max_cols)
            selected_col_indices = list(range(0, len(cols), step))
            if (len(cols) - 1) not in selected_col_indices:
                selected_col_indices.append(len(cols) - 1)
            df = df.iloc[:, selected_col_indices]
        return df


def solve_01_knapsack_dp(
    parcels: List[Parcel],
    weight_capacity: float,
    volume_capacity: Optional[float] = None,
    value_mode: str = "composite",
    scale_factor: float = 1.0
) -> KnapsackResult:
    """
    Solves the 0/1 Knapsack problem using Dynamic Programming.
    
    Parameters:
    - parcels: List of Candidate parcels (already prioritized)
    - weight_capacity: Maximum truck payload in kg
    - volume_capacity: Maximum truck volume in liters (optional secondary constraint)
    - value_mode: "composite" (uses composite priority score) or "monetary" (uses raw parcel value)
    - scale_factor: Discretization multiplier (e.g. 1.0 means 1 unit = 1 kg; 2.0 means 1 unit = 0.5 kg)
    
    Returns:
    - KnapsackResult object containing selected items, DP matrix, metrics, and execution time.
    """
    t0 = time.perf_counter()

    # Discretize weights to positive integers for DP table indexing
    scaled_capacity = max(1, int(round(weight_capacity * scale_factor)))
    n = len(parcels)

    weights = [max(1, int(round(p.weight * scale_factor))) for p in parcels]
    if value_mode == "monetary":
        values = [round(p.value, 2) for p in parcels]
    else:
        values = [round(p.composite_score, 2) for p in parcels]

    # Initialize DP table: (n + 1) rows x (scaled_capacity + 1) columns
    # dp[i][w] = max value attainable using subset of first i items with weight limit w
    dp = [[0.0 for _ in range(scaled_capacity + 1)] for _ in range(n + 1)]

    # Fill DP Table
    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(scaled_capacity + 1):
            if w < w_i:
                dp[i][w] = dp[i - 1][w]
            else:
                without_item = dp[i - 1][w]
                with_item = dp[i - 1][w - w_i] + v_i
                dp[i][w] = round(max(without_item, with_item), 2)

    # Backtracking to reconstruct optimal set of items
    selected_indices = []
    curr_w = scaled_capacity
    for i in range(n, 0, -1):
        # If value is different from row above, item i-1 was included
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            selected_indices.append(i - 1)
            curr_w -= weights[i - 1]

    selected_indices.reverse()

    # Separate selected and unselected
    selected_parcels = [parcels[idx] for idx in selected_indices]
    unselected_parcels = [parcels[idx] for idx in range(n) if idx not in selected_indices]

    # Handle volume capacity if specified (filter if volume exceeded)
    if volume_capacity is not None and volume_capacity > 0:
        vol_total = sum(p.volume for p in selected_parcels)
        if vol_total > volume_capacity:
            # Greedily prune lowest value-density parcels until volume constraint satisfied
            selected_parcels.sort(key=lambda p: p.composite_score / max(p.volume, 0.1))
            while vol_total > volume_capacity and selected_parcels:
                dropped = selected_parcels.pop(0)
                unselected_parcels.append(dropped)
                vol_total -= dropped.volume

    tot_weight = sum(p.weight for p in selected_parcels)
    tot_vol = sum(p.volume for p in selected_parcels)
    tot_val = sum(p.value if value_mode == "monetary" else p.composite_score for p in selected_parcels)

    elapsed_ms = (time.perf_counter() - t0) * 1000

    item_labels = ["Base (0 items)"] + [f"{p.id} ({p.weight}kg)" for p in parcels]
    weight_labels = list(range(scaled_capacity + 1))

    return KnapsackResult(
        selected_parcels=selected_parcels,
        unselected_parcels=unselected_parcels,
        total_weight=tot_weight,
        total_volume=tot_vol,
        total_value=tot_val,
        weight_capacity=weight_capacity,
        volume_capacity=volume_capacity or 0.0,
        dp_table=dp,
        weight_labels=weight_labels,
        item_labels=item_labels,
        execution_time_ms=elapsed_ms,
        scale_factor=scale_factor
    )


def solve_fractional_knapsack_greedy(
    parcels: List[Parcel],
    weight_capacity: float,
    value_mode: str = "composite"
) -> Dict[str, Any]:
    """
    Greedy Fractional Knapsack baseline algorithm for theoretical comparison.
    Sorts parcels by value/weight density and takes full or fractional parcels.
    Provides upper bound proof for DP comparison.
    """
    t0 = time.perf_counter()

    def get_val(p: Parcel) -> float:
        return p.value if value_mode == "monetary" else p.composite_score

    # Sort by ratio descending
    sorted_items = sorted(parcels, key=lambda p: get_val(p) / max(p.weight, 0.1), reverse=True)

    remaining_cap = weight_capacity
    total_val = 0.0
    fractions = {}

    for p in sorted_items:
        if remaining_cap <= 0:
            fractions[p.id] = 0.0
        elif p.weight <= remaining_cap:
            fractions[p.id] = 1.0
            total_val += get_val(p)
            remaining_cap -= p.weight
        else:
            frac = remaining_cap / p.weight
            fractions[p.id] = round(frac, 3)
            total_val += get_val(p) * frac
            remaining_cap = 0.0

    elapsed_ms = (time.perf_counter() - t0) * 1000
    return {
        "fractions": fractions,
        "upper_bound_value": round(total_val, 2),
        "execution_time_ms": round(elapsed_ms, 4)
    }
