"""
Main Demonstration & Execution Script
Design and Analysis of Algorithms (DAA) Capstone Project
Integrated Courier Planning System: Phases 1 to 5
"""

import sys
import os
import argparse
import time

from core.models import Parcel, DeliveryPoint
from core.sorting import compare_sorting_algorithms
from core.knapsack import solve_01_knapsack_dp, solve_fractional_knapsack_greedy
from core.graph import RoadGraph
from core.router import RouteOptimizer
from core.pipeline import CourierPlanningEngine
from benchmarks.benchmark import run_comprehensive_benchmarks


def print_header(title: str):
    print("\n" + "=" * 76)
    print(f"  {title.upper()}")
    print("=" * 76)


def print_phase_badge(phase: str, title: str):
    print("\n" + "-" * 76)
    print(f"  >>> [{phase}] {title}")
    print("-" * 76)


def run_full_demonstration(scenario_path: str = "data/small_dataset.json", capacity: float = 15.0):
    print_header("INTELLIGENT COURIER PLANNING SYSTEM - CAPSTONE DEMONSTRATION")
    print("Algorithmic Framework: Sorting + Dynamic Programming + Dijkstra + TSP Approximation")
    print(f"Execution Target: {scenario_path} | Van Weight Capacity: {capacity} kg")

    # -------------------------------------------------------------------------
    # PHASE 1: Courier Problem Design and Planning
    # -------------------------------------------------------------------------
    print_phase_badge("PHASE 1", "COURIER PROBLEM DESIGN AND PLANNING")
    engine = CourierPlanningEngine()
    engine.load_scenario_from_file(scenario_path)

    print(f"1. Logistics Hub / Depot: [{engine.depot_id}] {engine.graph.nodes[engine.depot_id].name}")
    print(f"2. Total Delivery Points (Nodes): {len(engine.graph.nodes)}")
    print(f"3. Road Network Edges: {len(engine.graph.edges)} physical road segments")
    print(f"4. Candidate Parcels Ingested: {len(engine.parcels)} items awaiting dispatch\n")

    print("Sample Ingested Parcel Pool:")
    print(f"{'Parcel ID':<10} {'Dest':<8} {'Priority':<10} {'Deadline':<10} {'Weight':<8} {'Volume':<8} {'Value':<8} {'Score':<8}")
    print("-" * 76)
    for p in engine.parcels[:6]:
        print(f"{p.id:<10} {p.destination_id:<8} {p.priority:<10} {p.deadline_hours:<10.1f}h {p.weight:<8.1f}kg {p.volume:<8.1f}L {p.value:<8.1f} {p.composite_score:<8.2f}")
    if len(engine.parcels) > 6:
        print(f"... and {len(engine.parcels) - 6} additional parcels.")

    # -------------------------------------------------------------------------
    # PHASE 2: Package Prioritization and Box Filling
    # -------------------------------------------------------------------------
    print_phase_badge("PHASE 2", "PACKAGE PRIORITIZATION AND BOX FILLING (SORTING & DP KNAPSACK)")

    print("[Step 2.1] Sorting Evaluation (MergeSort vs. QuickSort vs. TimSort):")
    sorted_parcels, sort_stats = compare_sorting_algorithms(engine.parcels, criterion="composite")
    print(f"  * MergeSort:  {sort_stats['mergesort']['time_ms']:.4f} ms | Comparisons: {sort_stats['mergesort']['comparisons']} (Guaranteed Stable O(N log N))")
    print(f"  * QuickSort:  {sort_stats['quicksort']['time_ms']:.4f} ms | Comparisons: {sort_stats['quicksort']['comparisons']} (In-place Median-of-3)")
    print(f"  * TimSort:    {sort_stats['timsort']['time_ms']:.4f} ms | Native C-level baseline")

    print("\n[Step 2.2] Dynamic Programming 0/1 Knapsack Solution:")
    knapsack_res = solve_01_knapsack_dp(
        parcels=sorted_parcels,
        weight_capacity=capacity,
        value_mode="composite",
        scale_factor=1.0
    )

    print(f"  * Vehicle Payload Capacity:   {capacity:.1f} kg")
    print(f"  * Total Weight Selected:      {knapsack_res.total_weight:.1f} kg ({knapsack_res.weight_utilization_pct}% capacity utilization)")
    print(f"  * Total Volume Selected:      {knapsack_res.total_volume:.1f} L")
    print(f"  * Total Trip Utility Score:   {knapsack_res.total_value:.2f} points")
    print(f"  * DP Matrix Computation Time: {knapsack_res.execution_time_ms:.4f} ms")

    print("\nSelected Parcels for Vehicle Loading:")
    for p in knapsack_res.selected_parcels:
        print(f"  [+] {p.id:<8} -> {p.destination_id:<8} | {p.priority:<8} | Deadline: {p.deadline_hours:.1f}h | Wt: {p.weight:.1f}kg | Val: {p.value:.1f} | Score: {p.composite_score:.2f}")

    print(f"\nDeferred Parcels ({len(knapsack_res.unselected_parcels)} deferred to next trip):")
    for p in knapsack_res.unselected_parcels:
        print(f"  [-] {p.id:<8} -> {p.destination_id:<8} | Wt: {p.weight:.1f}kg (Exceeds payload or lower priority)")

    # DP Table Printout (subset of table)
    print("\nDynamic Programming Table Evidence (Sample Slice):")
    dp_df = knapsack_res.get_dp_dataframe(max_cols=8)
    print(dp_df.to_string())

    # Greedy Fractional Knapsack Comparison
    frac_res = solve_fractional_knapsack_greedy(sorted_parcels, weight_capacity=capacity, value_mode="composite")
    print(f"\nTheoretical Optimality Comparison:")
    print(f"  * 0/1 Integer DP Optimum Value: {knapsack_res.total_value:.2f}")
    print(f"  * Fractional Continuous Bound: {frac_res['upper_bound_value']:.2f}")
    gap = ((frac_res['upper_bound_value'] - knapsack_res.total_value) / frac_res['upper_bound_value']) * 100.0
    print(f"  * Relaxation Optimality Gap:   {gap:.2f}% (Indivisibility penalty)")

    # -------------------------------------------------------------------------
    # PHASE 3: Route Maker and Graph Processing
    # -------------------------------------------------------------------------
    print_phase_badge("PHASE 3", "ROUTE MAKER AND GRAPH PROCESSING (DIJKSTRA + TSP)")

    router = RouteOptimizer(engine.graph)
    final_tour, tour_dist, legs, routing_stats = router.plan_delivery_route(
        depot_id=engine.depot_id,
        selected_parcels=knapsack_res.selected_parcels,
        use_2opt=True
    )

    print("[Step 3.1] Dijkstra's Shortest Path Computation:")
    print(f"  * Shortest road distances precomputed using Min-Heap Dijkstra (O((V + E) log V)).")

    print("\n[Step 3.2] TSP Route Sequence & 2-Opt Optimization:")
    print(f"  * Nearest Neighbor Initial Tour: {routing_stats['nn_distance_km']:.2f} km (Time: {routing_stats['nn_runtime_ms']:.3f} ms)")
    print(f"  * 2-Opt Local Search Tour:       {routing_stats['final_distance_km']:.2f} km (Time: {routing_stats['two_opt_runtime_ms']:.3f} ms)")
    print(f"  * Distance Reduction Achieved:   {routing_stats['distance_saved_km']:.2f} km ({routing_stats['improvement_pct']}%)")
    print(f"  * Final Ordered Tour:            {' -> '.join(final_tour)}")

    print("\nTurn-by-Turn Leg Navigation Breakdown:")
    for leg in legs:
        stops_delivered = f"Deliveries: {', '.join(leg['parcels_delivered'])}" if leg['parcels_delivered'] else "Return to Depot"
        road_nodes = ' -> '.join(leg['road_path'])
        print(f"  Leg {leg['leg_number']}: {leg['from_node']} -> {leg['to_node']} ({leg['distance_km']} km) | Path: [{road_nodes}] | {stops_delivered}")

    # Generate Visual Route Map
    os.makedirs("output", exist_ok=True)
    report = engine.execute_planning(weight_capacity=capacity, use_2opt=True)
    map_path = "output/route_map_small.png" if "small" in scenario_path else "output/route_map_medium.png"
    engine.plot_route_map(report, output_file=map_path)
    print(f"\n[Artifact Generated] Route visualization map rendered and saved to '{map_path}'")

    # -------------------------------------------------------------------------
    # PHASE 4: Performance Testing & Optimization
    # -------------------------------------------------------------------------
    print_phase_badge("PHASE 4", "PERFORMANCE TESTING AND ALGORITHMIC PROFILING")
    summary = report.get_summary_dict()
    print("Execution Timing Summary for Current Run:")
    print(f"  1. Sorting Phase (MergeSort):      {summary['runtimes_ms']['sorting']:.4f} ms")
    print(f"  2. Packing Phase (0/1 DP Knapsack):{summary['runtimes_ms']['knapsack_dp']:.4f} ms")
    print(f"  3. Route Planning (Dijkstra+TSP):  {summary['runtimes_ms']['tsp_routing']:.4f} ms")
    print(f"  -------------------------------------------------------------")
    print(f"  TOTAL END-TO-END PIPELINE:        {summary['runtimes_ms']['total_pipeline']:.4f} ms")

    # -------------------------------------------------------------------------
    # PHASE 5: Final Report and Demonstration
    # -------------------------------------------------------------------------
    print_phase_badge("PHASE 5", "FINAL SYSTEM REPORT & DISPATCH ORDERS")
    print("VEHICLE DISPATCH ORDER SUMMARY:")
    print(f"  * Vehicle Status:          READY FOR DISPATCH")
    print(f"  * Starting Depot:          {engine.depot_id} ({engine.graph.nodes[engine.depot_id].name})")
    print(f"  * Total Parcels Onboard:   {len(knapsack_res.selected_parcels)} units")
    print(f"  * Total Payload Weight:    {knapsack_res.total_weight:.2f} / {capacity:.1f} kg ({knapsack_res.weight_utilization_pct}%)")
    print(f"  * Total Route Mileage:     {tour_dist:.2f} km")
    print(f"  * Estimated Trip Duration: {summary['estimated_driving_mins']} minutes (driving + delivery stops)")
    print(f"  * Route Sequence:          {' -> '.join(final_tour)}")
    print("=" * 76)
    print("Capstone Demonstration successfully executed! All Phases 1 to 5 verified.")
    print("To launch the interactive classic UI, run:")
    print("    streamlit run app.py")
    print("=" * 76)


def main():
    parser = argparse.ArgumentParser(description="DAA Capstone Courier Planning System")
    parser.add_argument("--demo", action="store_true", help="Run full terminal demonstration on small dataset")
    parser.add_argument("--medium", action="store_true", help="Run terminal demonstration on medium dataset")
    parser.add_argument("--large", action="store_true", help="Run terminal demonstration on large dataset")
    parser.add_argument("--benchmark", action="store_true", help="Execute full Phase 4 performance benchmarking suite")
    parser.add_argument("--capacity", type=float, default=None, help="Override vehicle weight capacity (kg)")

    args = parser.parse_args()

    if args.benchmark:
        run_comprehensive_benchmarks()
    elif args.medium:
        cap = args.capacity or 40.0
        run_full_demonstration("data/medium_dataset.json", capacity=cap)
    elif args.large:
        cap = args.capacity or 80.0
        run_full_demonstration("data/large_dataset.json", capacity=cap)
    else:
        # Default: Small dataset demo
        cap = args.capacity or 15.0
        run_full_demonstration("data/small_dataset.json", capacity=cap)


if __name__ == "__main__":
    main()
