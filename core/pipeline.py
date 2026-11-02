"""
Integrated Courier Planning Pipeline Engine
Unifies Phase 1, Phase 2, Phase 3, Phase 4, and Phase 5 into an end-to-end workflow.
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from core.models import Parcel, DeliveryPoint, RoadEdge, DeliveryTrip
from core.sorting import compare_sorting_algorithms
from core.knapsack import solve_01_knapsack_dp, solve_fractional_knapsack_greedy, KnapsackResult
from core.graph import RoadGraph
from core.router import RouteOptimizer


class PipelineExecutionReport:
    """Consolidated results of an end-to-end courier planning run."""
    def __init__(
        self,
        parcels: List[Parcel],
        sorted_parcels: List[Parcel],
        sorting_stats: Dict[str, Any],
        knapsack_result: KnapsackResult,
        fractional_result: Dict[str, Any],
        tour_sequence: List[str],
        total_route_distance: float,
        detailed_legs: List[Dict[str, Any]],
        routing_stats: Dict[str, Any],
        graph: RoadGraph,
        depot_id: str,
        total_pipeline_time_ms: float
    ):
        self.parcels = parcels
        self.sorted_parcels = sorted_parcels
        self.sorting_stats = sorting_stats
        self.knapsack_result = knapsack_result
        self.fractional_result = fractional_result
        self.tour_sequence = tour_sequence
        self.total_route_distance = total_route_distance
        self.detailed_legs = detailed_legs
        self.routing_stats = routing_stats
        self.graph = graph
        self.depot_id = depot_id
        self.total_pipeline_time_ms = round(total_pipeline_time_ms, 3)

    def get_summary_dict(self) -> Dict[str, Any]:
        """Provides a clean dictionary summary for JSON export or console presentation."""
        return {
            "total_parcels_evaluated": len(self.parcels),
            "parcels_selected_for_trip": len(self.knapsack_result.selected_parcels),
            "parcels_deferred": len(self.knapsack_result.unselected_parcels),
            "total_cargo_weight_kg": self.knapsack_result.total_weight,
            "weight_capacity_kg": self.knapsack_result.weight_capacity,
            "weight_utilization_pct": self.knapsack_result.weight_utilization_pct,
            "total_cargo_volume_l": self.knapsack_result.total_volume,
            "volume_capacity_l": self.knapsack_result.volume_capacity,
            "volume_utilization_pct": self.knapsack_result.volume_utilization_pct,
            "total_trip_utility_value": self.knapsack_result.total_value,
            "fractional_upper_bound": self.fractional_result.get("upper_bound_value", 0.0),
            "tour_stops_count": len(self.tour_sequence),
            "total_route_distance_km": self.total_route_distance,
            "estimated_driving_mins": round((self.total_route_distance / 35.0) * 60.0 + len(self.knapsack_result.selected_parcels) * 4.0, 1),
            "runtimes_ms": {
                "sorting": self.sorting_stats.get("mergesort", {}).get("time_ms", 0.0),
                "knapsack_dp": self.knapsack_result.execution_time_ms,
                "tsp_routing": self.routing_stats.get("total_routing_ms", 0.0),
                "total_pipeline": self.total_pipeline_time_ms
            }
        }


class CourierPlanningEngine:
    """High-level facade orchestrating all phases of the Courier Planning System."""
    def __init__(self):
        self.parcels: List[Parcel] = []
        self.graph: RoadGraph = RoadGraph()
        self.depot_id: str = "DEPOT"

    def load_scenario_from_dict(self, data: Dict[str, Any]):
        """Populates the engine state from a scenario dictionary."""
        self.parcels = [Parcel.from_dict(p) for p in data.get("parcels", [])]
        self.graph = RoadGraph.create_from_nodes_and_edges(
            nodes_data=data.get("nodes", []),
            edges_data=data.get("edges", None)
        )
        depot = self.graph.get_depot()
        if depot:
            self.depot_id = depot.id
        elif "depot_id" in data:
            self.depot_id = data["depot_id"]

    def load_scenario_from_file(self, json_path: str):
        """Loads a scenario JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.load_scenario_from_dict(data)

    def execute_planning(
        self,
        weight_capacity: float,
        volume_capacity: Optional[float] = None,
        sort_criterion: str = "composite",
        use_2opt: bool = True,
        value_mode: str = "composite",
        scale_factor: float = 1.0
    ) -> PipelineExecutionReport:
        """
        Executes the full pipeline:
        1. Prioritize and sort parcels using MergeSort/QuickSort.
        2. Select optimal subset using 0/1 Knapsack DP.
        3. Solve TSP on customer graph using Dijkstra + Nearest Neighbor + 2-Opt.
        4. Measure runtimes and compile comprehensive report.
        """
        t_pipeline_start = time.perf_counter()

        # Step 1: Sorting
        sorted_parcels, sorting_stats = compare_sorting_algorithms(self.parcels, criterion=sort_criterion)

        # Step 2: Knapsack Dynamic Programming
        knapsack_res = solve_01_knapsack_dp(
            parcels=sorted_parcels,
            weight_capacity=weight_capacity,
            volume_capacity=volume_capacity,
            value_mode=value_mode,
            scale_factor=scale_factor
        )

        # Step 2b: Greedy baseline comparison
        fractional_res = solve_fractional_knapsack_greedy(
            parcels=sorted_parcels,
            weight_capacity=weight_capacity,
            value_mode=value_mode
        )

        # Step 3: Route Planning via Dijkstra and TSP
        router = RouteOptimizer(self.graph)
        final_tour, tour_distance, detailed_legs, routing_stats = router.plan_delivery_route(
            depot_id=self.depot_id,
            selected_parcels=knapsack_res.selected_parcels,
            use_2opt=use_2opt
        )

        total_time_ms = (time.perf_counter() - t_pipeline_start) * 1000

        return PipelineExecutionReport(
            parcels=self.parcels,
            sorted_parcels=sorted_parcels,
            sorting_stats=sorting_stats,
            knapsack_result=knapsack_res,
            fractional_result=fractional_res,
            tour_sequence=final_tour,
            total_route_distance=tour_distance,
            detailed_legs=detailed_legs,
            routing_stats=routing_stats,
            graph=self.graph,
            depot_id=self.depot_id,
            total_pipeline_time_ms=total_time_ms
        )

    def plot_route_map(
        self,
        report: PipelineExecutionReport,
        output_file: Optional[str] = None
    ) -> plt.Figure:
        """
        Generates an elegant, classic-styled visualization of the customer road network
        and the optimized delivery route.
        Adheres to non-radiant, human-engineered design principles:
        - Muted parchment/slate background
        - Oxford blue tour lines with subtle arrows
        - Classic dark green depot square, muted burgundy delivery stops
        - Clean serif typography and subtle grid lines
        """
        # Use classic styling
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='#FDFDFC')
        ax.set_facecolor('#F8F9FA')

        # 1. Plot all road network edges in subtle light slate
        for edge in self.graph.edges:
            if edge.source in self.graph.nodes and edge.destination in self.graph.nodes:
                u = self.graph.nodes[edge.source]
                v = self.graph.nodes[edge.destination]
                ax.plot([u.x, v.x], [u.y, v.y], color='#CBD5E1', linestyle='--', linewidth=1.0, zorder=1)

        # 2. Plot all physical nodes
        selected_dest_ids = set(p.destination_id for p in report.knapsack_result.selected_parcels)

        for node_id, node in self.graph.nodes.items():
            if node.is_depot or node_id == self.depot_id:
                # Depot: Classic dark forest green square
                ax.scatter(node.x, node.y, color='#1E4D2B', s=180, marker='s', edgecolors='#0D2818', linewidth=1.5, zorder=5)
                ax.text(node.x, node.y + 0.35, f"DEPOT: {node.name}", fontsize=9, fontweight='bold',
                        color='#1E4D2B', ha='center', va='bottom', fontfamily='serif')
            elif node_id in selected_dest_ids:
                # Selected customer: Classic deep brick red
                ax.scatter(node.x, node.y, color='#991B1B', s=120, marker='o', edgecolors='#450A0A', linewidth=1.5, zorder=5)
                ax.text(node.x, node.y + 0.3, node.id, fontsize=8, fontweight='bold',
                        color='#7F1D1D', ha='center', va='bottom', fontfamily='serif')
            else:
                # Unvisited node: Muted neutral gray
                ax.scatter(node.x, node.y, color='#94A3B8', s=50, marker='o', edgecolors='#475569', linewidth=1.0, zorder=3)
                ax.text(node.x, node.y - 0.3, node.id, fontsize=7, color='#64748B', ha='center', va='top')

        # 3. Plot the ordered delivery route with arrows
        tour = report.tour_sequence
        if len(tour) > 1:
            for i in range(len(tour) - 1):
                u_id = tour[i]
                v_id = tour[i + 1]
                if u_id in self.graph.nodes and v_id in self.graph.nodes:
                    u = self.graph.nodes[u_id]
                    v = self.graph.nodes[v_id]
                    
                    # Draw subtle curved or straight route segment
                    ax.annotate(
                        "",
                        xy=(v.x, v.y),
                        xytext=(u.x, u.y),
                        arrowprops=dict(
                            arrowstyle="-|>",
                            color='#1E3A8A',  # Classic Oxford Navy
                            lw=2.2,
                            mutation_scale=14,
                            alpha=0.85
                        ),
                        zorder=4
                    )
                    
                    # Label leg order
                    mid_x = (u.x + v.x) / 2.0
                    mid_y = (u.y + v.y) / 2.0
                    ax.text(
                        mid_x, mid_y, f"#{i+1}",
                        fontsize=7, color='#1E3A8A', fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.2", facecolor='#FFFFFF', edgecolor='#93C5FD', alpha=0.9),
                        ha='center', va='center', zorder=6
                    )

        ax.set_title(
            f"Courier Delivery Route Network\nTotal Distance: {report.total_route_distance:.2f} km | Stops: {len(tour)-1} | Parcels Delivered: {len(report.knapsack_result.selected_parcels)}",
            fontsize=12, fontweight='bold', color='#1E293B', pad=15, fontfamily='serif'
        )
        ax.set_xlabel("East-West Coordinate (km)", fontsize=9, color='#475569', fontfamily='serif')
        ax.set_ylabel("North-South Coordinate (km)", fontsize=9, color='#475569', fontfamily='serif')
        ax.grid(True, linestyle=':', alpha=0.6, color='#E2E8F0')

        # Classic custom legend
        depot_patch = patches.Patch(color='#1E4D2B', label='Dispatch Depot')
        dest_patch = patches.Patch(color='#991B1B', label='Active Delivery Stop')
        unvisited_patch = patches.Patch(color='#94A3B8', label='Unvisited Point')
        route_patch = patches.Patch(color='#1E3A8A', label='Optimized Delivery Route')
        ax.legend(handles=[depot_patch, dest_patch, unvisited_patch, route_patch],
                  loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8)

        plt.tight_layout()

        if output_file:
            fig.savefig(output_file, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')

        return fig

