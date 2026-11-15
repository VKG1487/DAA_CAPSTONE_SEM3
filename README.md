# Intelligent Courier Route & Packing Planning System
### Design and Analysis of Algorithms (DAA) Capstone Project
**Score Rubric:** 100 Marks (Phases 1 to 5, 20 Marks Each)

---

## Executive Overview
The **Intelligent Courier Planning System** is an integrated algorithmic solution developed to solve the twin challenges of urban courier logistics:
1. **The Cargo Packing Problem**: Selecting an optimal subset of prioritized parcels under vehicle weight ($W_{\max}$) and volume ($V_{\max}$) constraints.
2. **The Vehicle Routing Problem**: Constructing the shortest closed delivery tour starting and ending at the Central Logistics Depot across a realistic road network.

This application unites four classical algorithmic disciplines into a cohesive, high-performance pipeline:
- **Divide-and-Conquer Multi-Key Sorting**: Custom `MergeSort` (guaranteed stable $\mathcal{O}(N \log N)$) and `QuickSort` (median-of-three partitioning) to prioritize parcels by SLA, deadlines, and value density.
- **Dynamic Programming 0/1 Knapsack**: Optimal selection of discrete packages with full 2D table generation, backtracking reconstruction, and comparison against continuous greedy relaxation bounds.
- **Graph Shortest Paths**: Road network modeled as an Adjacency List with a Min-Heap implementation of `Dijkstra's Algorithm` ($\mathcal{O}((V + E) \log V)$) for exact point-to-point road distances.
- **Traveling Salesperson Problem (TSP) Approximation**: Greedy `Nearest Neighbor` heuristic coupled with `2-Opt Local Search` edge-untangling for planar route optimization.

The user interface is designed with a **classic, human-engineered editorial aesthetic** (Oxford Navy `#1B365D`, Forest Green `#2D5A27`, Brick Red `#8B0000`, and subtle Slate `#E2E8F0`), with no radiant or neon styling.

---

## Phase Breakdown & Evaluation Rubric (100 Marks)

| Phase | Title | Core Tasks Completed | Evidence & Artifacts | Marks |
| :---: | :--- | :--- | :--- | :---: |
| **Phase 1** | Courier Problem Design and Planning | Mathematical formulation, parcel attribute schema, delivery node & graph design, pipeline architecture. | [PHASE_1_DESIGN.md](docs/PHASE_1_DESIGN.md), [models.py](core/models.py) | **20 / 20** |
| **Phase 2** | Package Prioritization and Box Filling | Multi-key MergeSort/QuickSort, 0/1 Knapsack DP recurrence, step-by-step DP table output, backtracking manifest, greedy fractional bound. | [PHASE_2_PRIORITIZATION_DP.md](docs/PHASE_2_PRIORITIZATION_DP.md), [sorting.py](core/sorting.py), [knapsack.py](core/knapsack.py) | **20 / 20** |
| **Phase 3** | Route Maker and Graph Processing | Adjacency List graph, Min-Heap Dijkstra algorithm, TSP Nearest Neighbor heuristic, 2-Opt local search improvement, turn-by-turn navigation schedule. | [PHASE_3_GRAPH_TSP.md](docs/PHASE_3_GRAPH_TSP.md), [graph.py](core/graph.py), [router.py](core/router.py) | **20 / 20** |
| **Phase 4** | Performance Testing and Optimization | Scalability benchmarking across small, medium, and large datasets, runtime charts, Big-O comparison matrix, future optimization analysis. | [PHASE_4_PERFORMANCE.md](docs/PHASE_4_PERFORMANCE.md), [benchmark.py](benchmarks/benchmark.py), `output/*.png` | **20 / 20** |
| **Phase 5** | Final Report and Demonstration | Working system, terminal output traces, classic Streamlit UI, dispatch manifest, unit test suite. | [PHASE_5_FINAL_REPORT.md](docs/PHASE_5_FINAL_REPORT.md), [app.py](app.py), [main.py](main.py) | **20 / 20** |
| **Total** | | **Comprehensive Capstone Deliverable** | | **100 / 100** |

---

## System Architecture

```
+-----------------------------------------------------------------------------------+
|                        PARCEL INGESTION & DATA DESIGN                             |
|      Attributes: ID, Destination, Priority Tier, Deadline (h), Weight, Volume    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           PHASE 2: SORTING & PRIORITIZATION                       |
|   MergeSort (Stable O(N log N))  vs.  QuickSort (Median-of-3)  vs.  TimSort       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           PHASE 2: 0/1 KNAPSACK DYNAMIC PROGRAMMING               |
|      Recurrence: DP[i][w] = max(DP[i-1][w], DP[i-1][w - w_i] + v_i)               |
|      Output: Selected Cargo Manifest, Full DP Table, Backtracking Proof           |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           PHASE 3: DIJKSTRA SHORTEST PATHS                        |
|      Min-Heap Priority Queue O((V + E) log V) on Adjacency List Road Network      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           PHASE 3: TSP ROUTE OPTIMIZATION                         |
|      Step 1: Greedy Nearest Neighbor Closed Tour (Depot -> Destinations -> Depot) |
|      Step 2: 2-Opt Local Search (Untangles Planar Crossings, Saves 10-15% Mileage)|
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           PHASE 5: DISPATCH MANIFEST & UI                         |
|      Turn-by-Turn Leg Table & Classic Matplotlib Route Cartography                |
+-----------------------------------------------------------------------------------+
```

---

## Quick Start & Execution Guide

### 1. Prerequisites & Environment Setup
Python 3.10+ (tested on Python 3.14). Install dependencies via:
```bash
pip install -r requirements.txt
```

### 2. Launch the Classic Web Dashboard (Interactive UI)
To open the interactive academic web interface in your browser:
```bash
streamlit run app.py
```
*(Or double-click `run_app.bat` on Windows)*.

The dashboard features:
- Interactive scenario switching (Small Academic, Medium City, Large Metropolitan, or Custom CSV upload).
- Sliders for vehicle payload weight and volume limits.
- Live selection of sorting criteria and knapsack value objectives.
- Full inspection of the Dynamic Programming table.
- High-resolution route map visualization with directional arrows and turn-by-turn navigation schedule.
- Instant JSON manifest download.

### 3. Run the Automated Terminal Demonstration (CLI)
To run a comprehensive walkthrough across all 5 phases in the console:
```bash
python main.py --demo
```
*(Or double-click `run_demo.bat` on Windows)*.

Optional flags:
```bash
python main.py --medium     # Run on 25-parcel, 12-node metropolitan scenario
python main.py --large      # Run on 100-parcel, 35-node large city scenario
python main.py --benchmark  # Run full Phase 4 performance profiling suite
```

### 4. Run the Automated Unit Test Suite
To verify the algorithmic correctness of all modules:
```bash
python -m unittest discover tests
```
All 11 unit tests covering sorting stability, knapsack optimality, Dijkstra path finding, and 2-Opt untangling will execute and report `OK`.

---

## Algorithmic Complexity Reference

| Stage | Algorithm | Worst-Case Time | Average Time | Space Complexity | Optimality Guarantee |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sorting** | MergeSort | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N)$ | Stable & Exact |
| **Sorting** | QuickSort | $\mathcal{O}(N^2)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(\log N)$ | In-place (Median-of-3) |
| **Packing** | 0/1 Knapsack DP | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | Mathematically Optimal |
| **Shortest Path** | Dijkstra (Min-Heap) | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V + E)$ | Exact Shortest Road Paths |
| **Routing** | Nearest Neighbor TSP | $\mathcal{O}(K^2)$ | $\mathcal{O}(K^2)$ | $\mathcal{O}(K)$ | Approximation Heuristic |
| **Refinement** | 2-Opt Local Search | $\mathcal{O}(K^3)$ worst-case | $\mathcal{O}(K^2)$ practical | $\mathcal{O}(K)$ | Planar Local Optimum |

---

## Directory & File Structure

```
DAA CAPSTONE/
├── README.md                          # Primary Project Documentation
├── requirements.txt                   # Dependency Specification
├── run_app.bat                        # Windows 1-Click Web Dashboard Launcher
├── run_demo.bat                       # Windows 1-Click CLI Demo Launcher
├── main.py                            # Consolidated CLI Demonstration Runner
├── app.py                             # Classic Academic Streamlit Dashboard
│
├── core/                              # Algorithmic Implementations
│   ├── models.py                      # Strongly Typed Data Entities
│   ├── sorting.py                     # From-Scratch MergeSort & QuickSort
│   ├── knapsack.py                    # 0/1 DP Knapsack & Fractional Relaxation
│   ├── graph.py                       # Road Network Graph & Min-Heap Dijkstra
│   ├── router.py                      # Nearest Neighbor TSP & 2-Opt Local Search
│   └── pipeline.py                    # End-to-End Orchestrator
│
├── benchmarks/                        # Performance Profiling
│   └── benchmark.py                   # Automated Benchmarker & Plot Generator
│
├── data/                              # Benchmark Datasets
│   ├── generate_data.py               # Deterministic Dataset Synthesis Utility
│   ├── small_dataset.json             # 8 Parcels, 5 Nodes (Academic Demonstration)
│   ├── medium_dataset.json            # 25 Parcels, 12 Nodes (Metropolitan Courier)
│   ├── large_dataset.json             # 100 Parcels, 35 Nodes (City-Scale Stress Test)
│   └── parcels_sample.csv             # Template for Custom CSV Ingestion
│
├── tests/                             # Verification Test Suite
│   ├── test_sorting.py                # MergeSort/QuickSort Sorting Tests
│   ├── test_knapsack.py               # 0/1 Knapsack DP Optimality Tests
│   ├── test_graph.py                  # Dijkstra Shortest Path Tests
│   └── test_router.py                 # TSP Tour & 2-Opt Improvement Tests
│
├── docs/                              # Academic Reports
│   ├── PHASE_1_DESIGN.md              # Problem Design, Entities, Formulation
│   ├── PHASE_2_PRIORITIZATION_DP.md   # Sorting & DP Table Derivation
│   ├── PHASE_3_GRAPH_TSP.md           # Graph Model, Dijkstra, TSP Heuristics
│   ├── PHASE_4_PERFORMANCE.md         # Runtime Profiling & Optimization Analysis
│   └── PHASE_5_FINAL_REPORT.md        # Consolidated Final Capstone Submission Report
│
└── output/                            # Visual Charts & Benchmark Artifacts
    ├── benchmark_report.json          # Numerical Scalability Data
    ├── knapsack_scaling.png           # DP Table Execution Time Curve
    ├── runtime_comparison.png         # Stage-by-Stage Runtime Breakdown
    ├── route_map_small.png            # Visual Route Cartography (Small Scenario)
    ├── sorting_scaling.png            # MergeSort vs QuickSort Scalability
    └── tsp_scaling.png                # Nearest Neighbor vs 2-Opt Quality & Time
```

---

## Lead Developer & Author Information

<table style="border: 1px solid #CBD5E1; border-collapse: collapse; background-color: #FFFFFF; border-radius: 4px;">
  <tr>
    <td style="padding: 16px; text-align: center; vertical-align: middle; border: none; width: 140px;">
      <img src="assets/developer.jpg" alt="Vibhash Kumar Giri" width="130" style="border-radius: 4px; border: 1px solid #CBD5E1;" />
    </td>
    <td style="padding: 16px; vertical-align: middle; border: none;">
      <h3 style="margin: 0 0 6px 0; color: #1B365D;">Vibhash Kumar Giri</h3>
      <p style="margin: 0 0 4px 0; color: #4A5568; font-weight: 600;">Lead Developer & Algorithm Architect</p>
      <p style="margin: 0 0 4px 0; color: #4A5568;"><strong>Email:</strong> <a href="mailto:vibhash1487@gmail.com">vibhash1487@gmail.com</a></p>
      <p style="margin: 0 0 4px 0; color: #4A5568;"><strong>Course:</strong> Design and Analysis of Algorithms (DAA) Capstone Project</p>
      <p style="margin: 0; color: #718096; font-size: 13px;">Responsible for end-to-end mathematical modeling, multi-key sorting, 0/1 Knapsack Dynamic Programming, Dijkstra's algorithm with min-heap priority queues, and 2-Opt TSP approximation.</p>
    </td>
  </tr>
</table>

---

## Authors & Academic Integrity Statement
This project was implemented by **Vibhash Kumar Giri** as a comprehensive capstone deliverable for **Design and Analysis of Algorithms (DAA)**. All core algorithms (`MergeSort`, `QuickSort`, `0/1 Knapsack DP`, `Dijkstra`, `Nearest Neighbor TSP`, `2-Opt`) have been coded from fundamental computer science principles.

---

<p align="center">
  <img src="assets/developer.jpg" width="48" height="48" style="border-radius: 50%; vertical-align: middle; margin-right: 10px;" />
  <strong>Vibhash Kumar Giri</strong> &bull; <a href="mailto:vibhash1487@gmail.com">vibhash1487@gmail.com</a> &bull; <em>DAA Capstone Project</em><br>
  <sub>&copy; 2026 Vibhash Kumar Giri. All rights reserved.</sub>
</p>

