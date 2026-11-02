"""
Performance Testing and Optimization Benchmark Suite
Phase 4: Performance Testing and Optimization
Measures execution times of all algorithmic components, generates scaling charts,
and exports comparative analytics.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import json
import random
import matplotlib.pyplot as plt
import numpy as np

from core.models import Parcel, DeliveryPoint
from core.sorting import MergeSort, QuickSort, get_sort_key_fn
from core.knapsack import solve_01_knapsack_dp
from core.graph import RoadGraph
from core.router import RouteOptimizer
from core.pipeline import CourierPlanningEngine


def run_comprehensive_benchmarks(output_dir: str = "output") -> dict:
    """
    Executes automated performance benchmarks across all algorithmic phases:
    1. Sorting scaling (MergeSort vs QuickSort vs TimSort)
    2. Knapsack DP scaling (N x W)
    3. Dijkstra Shortest Path scaling
    4. TSP Nearest Neighbor vs 2-Opt route optimization
    5. Integrated pipeline comparative execution
    """
    os.makedirs(output_dir, exist_ok=True)
    random.seed(101)

    print("===============================================================")
    print("      DAA CAPSTONE: PHASE 4 PERFORMANCE BENCHMARKING          ")
    print("===============================================================")

    # -------------------------------------------------------------------------
    # 1. SORTING BENCHMARK
    # -------------------------------------------------------------------------
    print("\n[Phase 4.1] Benchmarking Sorting Algorithms (MergeSort vs QuickSort vs TimSort)...")
    sort_sizes = [10, 25, 50, 100, 250, 500, 1000]
    mergesort_times = []
    quicksort_times = []
    timsort_times = []
    mergesort_comps = []
    quicksort_comps = []

    ms = MergeSort()
    qs = QuickSort()
    key_fn = get_sort_key_fn("composite")

    for n in sort_sizes:
        test_parcels = [
            Parcel(
                id=f"P-{i}",
                destination_id=f"LOC-{i%10}",
                priority=random.choice(["Critical", "High", "Medium", "Low"]),
                deadline_hours=round(random.uniform(1.0, 12.0), 1),
                weight=round(random.uniform(1.0, 10.0), 1),
                volume=round(random.uniform(2.0, 20.0), 1),
                value=round(random.uniform(10.0, 100.0), 1)
            ) for i in range(n)
        ]

        # MergeSort
        t0 = time.perf_counter()
        ms.sort(test_parcels, key_fn)
        mergesort_times.append((time.perf_counter() - t0) * 1000)
        mergesort_comps.append(ms.comparisons)

        # QuickSort
        t0 = time.perf_counter()
        qs.sort(test_parcels, key_fn)
        quicksort_times.append((time.perf_counter() - t0) * 1000)
        quicksort_comps.append(qs.comparisons)

        # TimSort
        t0 = time.perf_counter()
        sorted(test_parcels, key=key_fn)
        timsort_times.append((time.perf_counter() - t0) * 1000)

    # -------------------------------------------------------------------------
    # 2. KNAPSACK DP BENCHMARK
    # -------------------------------------------------------------------------
    print("\n[Phase 4.2] Benchmarking 0/1 Knapsack Dynamic Programming (N x W)...")
    knapsack_n_sizes = [5, 10, 20, 35, 50, 75, 100]
    knapsack_capacity = 50.0  # kg
    knapsack_times = []
    cell_evaluations = []

    for n in knapsack_n_sizes:
        test_items = [
            Parcel(
                id=f"PK-{i}",
                destination_id=f"LOC-{i}",
                priority="High",
                deadline_hours=3.0,
                weight=round(random.uniform(1.0, 8.0), 1),
                volume=5.0,
                value=round(random.uniform(20.0, 80.0), 1)
            ) for i in range(n)
        ]
        t0 = time.perf_counter()
        res = solve_01_knapsack_dp(test_items, weight_capacity=knapsack_capacity, scale_factor=1.0)
        elapsed = (time.perf_counter() - t0) * 1000
        knapsack_times.append(elapsed)
        cell_evaluations.append((n + 1) * (int(knapsack_capacity) + 1))

    # -------------------------------------------------------------------------
    # 3. DIJKSTRA GRAPH BENCHMARK
    # -------------------------------------------------------------------------
    print("\n[Phase 4.3] Benchmarking Dijkstra's Shortest Path Algorithm (V log V + E)...")
    dijkstra_v_sizes = [5, 10, 20, 35, 50, 80]
    dijkstra_times = []

    for v in dijkstra_v_sizes:
        nodes_data = [
            {"id": f"N-{i}", "name": f"Node {i}", "x": random.uniform(-10, 10), "y": random.uniform(-10, 10), "is_depot": (i==0)}
            for i in range(v)
        ]
        g = RoadGraph.create_from_nodes_and_edges(nodes_data)
        t0 = time.perf_counter()
        g.dijkstra("N-0")
        dijkstra_times.append((time.perf_counter() - t0) * 1000)

    # -------------------------------------------------------------------------
    # 4. TSP ROUTING BENCHMARK (NN vs 2-Opt)
    # -------------------------------------------------------------------------
    print("\n[Phase 4.4] Benchmarking TSP Route Optimization (Nearest Neighbor vs 2-Opt)...")
    tsp_stops_sizes = [4, 6, 8, 12, 16, 20, 25]
    nn_times = []
    opt2_times = []
    nn_distances = []
    opt2_distances = []

    # Create reference graph with 30 nodes
    ref_nodes = [{"id": f"S-{i}", "name": f"Stop {i}", "x": random.uniform(-15, 15), "y": random.uniform(-15, 15), "is_depot": (i==0)} for i in range(30)]
    ref_graph = RoadGraph.create_from_nodes_and_edges(ref_nodes)
    router = RouteOptimizer(ref_graph)

    for k in tsp_stops_sizes:
        stops = [
            Parcel(id=f"P-{i}", destination_id=f"S-{i+1}", priority="High", deadline_hours=2.0, weight=2.0, volume=3.0, value=50.0)
            for i in range(k)
        ]
        _, _, _, stats = router.plan_delivery_route("S-0", stops, use_2opt=True)
        nn_times.append(stats["nn_runtime_ms"])
        opt2_times.append(stats["two_opt_runtime_ms"])
        nn_distances.append(stats["nn_distance_km"])
        opt2_distances.append(stats["final_distance_km"])

    # -------------------------------------------------------------------------
    # 5. INTEGRATED SCENARIO BENCHMARK (Small, Medium, Large)
    # -------------------------------------------------------------------------
    print("\n[Phase 4.5] Benchmarking End-to-End Pipeline on Standard Scenarios...")
    scenarios = [
        ("Small (8 parcels, 5 nodes)", "data/small_dataset.json", 15.0),
        ("Medium (25 parcels, 12 nodes)", "data/medium_dataset.json", 40.0),
        ("Large (100 parcels, 35 nodes)", "data/large_dataset.json", 80.0),
    ]

    scenario_results = []
    engine = CourierPlanningEngine()

    for name, path, cap in scenarios:
        engine.load_scenario_from_file(path)
        report = engine.execute_planning(weight_capacity=cap, use_2opt=True)
        summary = report.get_summary_dict()
        summary["scenario_name"] = name
        scenario_results.append(summary)

    # -------------------------------------------------------------------------
    # PLOTTING CLASSIC-STYLE CHARTS
    # -------------------------------------------------------------------------
    print("\nGenerating publication-quality, classic-styled runtime charts...")

    # Chart 1: Sorting Scaling
    plt.figure(figsize=(8, 5), facecolor='#FDFDFC')
    ax = plt.gca()
    ax.set_facecolor('#F8F9FA')
    plt.plot(sort_sizes, mergesort_times, 'o-', color='#1B365D', label='MergeSort (O(N log N))', lw=1.8)
    plt.plot(sort_sizes, quicksort_times, 's--', color='#8B0000', label='QuickSort Median-of-3', lw=1.8)
    plt.plot(sort_sizes, timsort_times, '^:', color='#2D5A27', label='Python TimSort (C-Optimized)', lw=1.8)
    plt.title('Sorting Algorithm Scalability Comparison', fontsize=11, fontweight='bold', color='#1E293B', pad=12, fontfamily='serif')
    plt.xlabel('Number of Parcels (N)', fontsize=9, color='#475569', fontfamily='serif')
    plt.ylabel('Execution Time (milliseconds)', fontsize=9, color='#475569', fontfamily='serif')
    plt.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    plt.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8)
    plt.tight_layout()
    sort_chart_path = os.path.join(output_dir, 'sorting_scaling.png')
    plt.savefig(sort_chart_path, dpi=300)
    plt.close()

    # Chart 2: Knapsack DP Scaling
    plt.figure(figsize=(8, 5), facecolor='#FDFDFC')
    ax = plt.gca()
    ax.set_facecolor('#F8F9FA')
    plt.plot(knapsack_n_sizes, knapsack_times, 'o-', color='#1B365D', label='0/1 Knapsack DP Table Fill', lw=2.0)
    plt.title(f'0/1 Knapsack DP Runtime Scaling (Capacity W = {int(knapsack_capacity)} kg)', fontsize=11, fontweight='bold', color='#1E293B', pad=12, fontfamily='serif')
    plt.xlabel('Number of Candidate Parcels (N)', fontsize=9, color='#475569', fontfamily='serif')
    plt.ylabel('Execution Time (milliseconds)', fontsize=9, color='#475569', fontfamily='serif')
    plt.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    plt.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8)
    plt.tight_layout()
    knapsack_chart_path = os.path.join(output_dir, 'knapsack_scaling.png')
    plt.savefig(knapsack_chart_path, dpi=300)
    plt.close()

    # Chart 3: TSP Distance & Runtime Trade-off
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#FDFDFC')
    ax1.set_facecolor('#F8F9FA')
    ax2.set_facecolor('#F8F9FA')

    # Distance Comparison
    ax1.plot(tsp_stops_sizes, nn_distances, 'o--', color='#8B0000', label='Nearest Neighbor Tour (km)', lw=1.8)
    ax1.plot(tsp_stops_sizes, opt2_distances, 's-', color='#1B365D', label='2-Opt Optimized Tour (km)', lw=2.0)
    ax1.set_title('Route Distance Quality: NN vs 2-Opt', fontsize=10, fontweight='bold', color='#1E293B', fontfamily='serif')
    ax1.set_xlabel('Number of Delivery Stops (K)', fontsize=9, color='#475569', fontfamily='serif')
    ax1.set_ylabel('Total Route Distance (km)', fontsize=9, color='#475569', fontfamily='serif')
    ax1.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8)

    # Runtime Comparison
    ax2.plot(tsp_stops_sizes, nn_times, 'o--', color='#2D5A27', label='Nearest Neighbor Time (ms)', lw=1.8)
    ax2.plot(tsp_stops_sizes, opt2_times, 's-', color='#6B21A8', label='2-Opt Search Time (ms)', lw=2.0)
    ax2.set_title('TSP Execution Runtime Comparison', fontsize=10, fontweight='bold', color='#1E293B', fontfamily='serif')
    ax2.set_xlabel('Number of Delivery Stops (K)', fontsize=9, color='#475569', fontfamily='serif')
    ax2.set_ylabel('Runtime (milliseconds)', fontsize=9, color='#475569', fontfamily='serif')
    ax2.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax2.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8)

    plt.tight_layout()
    tsp_chart_path = os.path.join(output_dir, 'tsp_scaling.png')
    plt.savefig(tsp_chart_path, dpi=300)
    plt.close()

    # Chart 4: Component Runtime Breakdown across Scenarios
    plt.figure(figsize=(9, 5), facecolor='#FDFDFC')
    ax = plt.gca()
    ax.set_facecolor('#F8F9FA')

    scenario_labels = ["Small (8 pkgs)", "Medium (25 pkgs)", "Large (100 pkgs)"]
    sorting_bars = [s["runtimes_ms"]["sorting"] for s in scenario_results]
    knapsack_bars = [s["runtimes_ms"]["knapsack_dp"] for s in scenario_results]
    routing_bars = [s["runtimes_ms"]["tsp_routing"] for s in scenario_results]

    x = np.arange(len(scenario_labels))
    width = 0.25

    ax.bar(x - width, sorting_bars, width, label='Sorting (MergeSort)', color='#1B365D')
    ax.bar(x, knapsack_bars, width, label='Packing (0/1 Knapsack DP)', color='#8B0000')
    ax.bar(x + width, routing_bars, width, label='Routing (Dijkstra + TSP)', color='#2D5A27')

    ax.set_title('Algorithmic Component Execution Time Breakdown', fontsize=11, fontweight='bold', color='#1E293B', pad=12, fontfamily='serif')
    ax.set_xlabel('Problem Dataset Scenario', fontsize=9, color='#475569', fontfamily='serif')
    ax.set_ylabel('Time (milliseconds)', fontsize=9, color='#475569', fontfamily='serif')
    ax.set_xticks(x)
    ax.set_xticklabels(scenario_labels, fontsize=9, fontfamily='serif')
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1', axis='y')
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8)

    plt.tight_layout()
    comp_chart_path = os.path.join(output_dir, 'runtime_comparison.png')
    plt.savefig(comp_chart_path, dpi=300)
    plt.close()

    # Save structured benchmark report
    benchmark_data = {
        "sorting": {
            "sizes": sort_sizes,
            "mergesort_times_ms": [round(t, 4) for t in mergesort_times],
            "quicksort_times_ms": [round(t, 4) for t in quicksort_times],
            "timsort_times_ms": [round(t, 4) for t in timsort_times],
            "mergesort_comparisons": mergesort_comps,
            "quicksort_comparisons": quicksort_comps
        },
        "knapsack_dp": {
            "n_items": knapsack_n_sizes,
            "capacity_kg": knapsack_capacity,
            "runtimes_ms": [round(t, 4) for t in knapsack_times],
            "cell_evaluations": cell_evaluations
        },
        "dijkstra": {
            "v_nodes": dijkstra_v_sizes,
            "runtimes_ms": [round(t, 4) for t in dijkstra_times]
        },
        "tsp_routing": {
            "k_stops": tsp_stops_sizes,
            "nn_times_ms": [round(t, 4) for t in nn_times],
            "two_opt_times_ms": [round(t, 4) for t in opt2_times],
            "nn_distances_km": nn_distances,
            "opt2_distances_km": opt2_distances
        },
        "scenarios": scenario_results
    }

    report_path = os.path.join(output_dir, "benchmark_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2)

    print(f"\nAll benchmark charts saved successfully in '{output_dir}/'")
    print(f"Benchmark summary JSON saved to '{report_path}'")
    return benchmark_data


if __name__ == "__main__":
    run_comprehensive_benchmarks()
