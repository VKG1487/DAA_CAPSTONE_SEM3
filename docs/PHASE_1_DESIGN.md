# Phase 1: Courier Problem Design and Planning

**Course:** Design and Analysis of Algorithms (DAA) Capstone Project  
**Lead Developer:** Vibhash Kumar Giri  
**Contact Email:** vibhash1487@gmail.com  
**Module:** Courier Problem Design and Planning  
**Marks Allocation:** 20 Marks  

---

## 1. Executive Problem Definition

In modern logistics and last-mile courier fulfillment, an urban dispatch center faces a constrained multi-criteria resource allocation and spatial routing challenge. Each morning or dispatch window, hundreds of parcels arrive at a central logistics depot with disparate delivery deadlines, physical dimensions (weight, volume), priority service tiers, and geographical delivery destinations across a metropolitan road network.

A single delivery vehicle (e.g., standard courier van) possesses strict physical capacity constraints:
1. **Maximum Payload Weight Limit ($W_{\max}$ in kg)**
2. **Maximum Cargo Volume Limit ($V_{\max}$ in Liters)**

The objective of the **Intelligent Courier Planning System** is to maximize the aggregate customer delivery utility (prioritizing critical, urgent, and high-value packages) while minimizing the total vehicle travel distance, dispatch time, and fuel consumption over a physical road network.

---

## 2. Integrated Algorithmic Workflow

To solve this problem, four classical algorithmic paradigms are pipelined in sequence:

```
+-------------------------------------------------------------------------------+
|                      INCOMING CANDIDATE PARCEL POOL                           |
|                      (Parcels P_1, P_2, ..., P_N)                             |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 2.1: MULTI-KEY SORTING                                                  |
| Algorithm: MergeSort / QuickSort (Divide-and-Conquer)                         |
| Objective: Rank parcels by composite priority (Deadline + Tier + Density)     |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 2.2: BOX FILLING & CARGO SELECTION                                      |
| Algorithm: 0/1 Knapsack Dynamic Programming                                   |
| Objective: Select optimal parcel subset S maximizing utility within W_max     |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 3.1: SHORTEST PATH ROAD METRIC DERIVATION                               |
| Algorithm: Dijkstra's Algorithm with Min-Heap Priority Queue                  |
| Objective: Compute all-pairs shortest road distances and physical node paths |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 3.2: DELIVERY ROUTE PLANNING & OPTIMIZATION                             |
| Algorithm: Nearest Neighbor TSP Heuristic + 2-Opt Local Search                |
| Objective: Find minimal-distance closed delivery tour starting/ending at Depot|
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 5: VEHICLE DISPATCH MANIFEST & TURN-BY-TURN NAVIGATION                  |
+-------------------------------------------------------------------------------+
```

---

## 3. Data Schema and Entity Specifications

### 3.1 Parcel Entity Attributes
Each package $p_i \in \mathcal{P}$ is parameterized by the following schema:
- **`id` (str)**: Unique tracking identifier (e.g., `PKG-01`).
- **`destination_id` (str)**: Target customer delivery node in the road network graph.
- **`priority` (str)**: Service-level agreement category:
  - `Critical` (Multiplier = 4): Emergency medical specimens, sensitive legal instruments.
  - `High` (Multiplier = 3): Server components, mission-critical commercial orders.
  - `Medium` (Multiplier = 2): Standard retail e-commerce goods.
  - `Low` (Multiplier = 1): Non-urgent marketing or bulk goods.
- **`deadline_hours` ($T_{\text{due}}$ in hours)**: Guaranteed delivery cutoff from dispatch.
- **`weight` ($w_i$ in kg)**: Physical mass of parcel.
- **`volume` ($v_i$ in L)**: Space occupied in cubic decimeters / liters.
- **`value` ($u_i$ in points/$)**: Declared economic worth or non-delivery penalty.
- **`composite_score`**: Synthesized prioritization metric calculated as:
  $$\text{Score}(p_i) = \frac{10}{T_{\text{due}} + 0.5} + 5 \cdot \text{PriorityWeight}(p_i) + \frac{u_i}{\max(w_i, 0.1)}$$

### 3.2 Delivery Point (Node) Attributes
Each point $v_j \in \mathcal{V}$ in the city map represents either the dispatch depot or a customer destination:
- **`id` (str)**: Node label (e.g., `DEPOT`, `LOC-A`, `LOC-B`).
- **`name` (str)**: Human-readable location description (e.g., "Metro General Hospital").
- **`x`, `y` (float)**: Cartesian spatial coordinates in kilometers for 2D topology and planar visualization.
- **`is_depot` (bool)**: Flag designating the central dispatch and return terminal.
- **`service_time_mins` (float)**: Fixed dwell time required for physical parcel drop-off (default: 4-5 mins).

### 3.3 Road Edge Attributes
A road segment $e = (u, v) \in \mathcal{E}$ connects two nodes:
- **`source` (str)**: Starting node identifier.
- **`destination` (str)**: Terminating node identifier.
- **`distance` (float in km)**: Actual road driving distance (incorporating street curvature and tortuosity).
- **`bidirectional` (bool)**: Indicates two-way traffic flow.

---

## 4. Algorithmic Selection & Theoretical Suitability

| System Component | Selected Algorithm | Alternative Rejected | Rationale for Selection |
| :--- | :--- | :--- | :--- |
| **Parcel Prioritization** | **MergeSort** (Divide & Conquer) | BubbleSort / InsertionSort | Guarantees worst-case $\mathcal{O}(N \log N)$ runtime and is **stable**, preserving tie-break ordering among equal deadlines. |
| **Vehicle Packing** | **0/1 Knapsack DP** (Dynamic Programming) | Greedy Fractional Knapsack | Parcels are discrete/indivisible ($x_i \in \{0, 1\}$). Greedy approaches make irreversible suboptimal choices due to indivisibility. DP guarantees mathematical global optimality. |
| **Shortest Road Paths** | **Dijkstra's Algorithm** (Min-Heap) | Bellman-Ford / Floyd-Warshall | Road distances are strictly non-negative ($w(u, v) > 0$). Dijkstra with a binary min-heap runs in $\mathcal{O}((V + E) \log V)$, vastly outperforming Bellman-Ford's $\mathcal{O}(V \cdot E)$. |
| **Delivery Route Tour** | **Nearest Neighbor + 2-Opt** (Approximation) | Brute-force TSP ($O(N!)$) / Held-Karp ($O(2^N N^2)$) | TSP is NP-Hard. For $K \ge 15$ delivery stops, exact enumeration requires billions of operations. Nearest Neighbor generates a greedy tour in $\mathcal{O}(K^2)$, and 2-Opt local search removes intersecting planar crossings in polynomial time. |

---

## 5. Architectural Correctness Criteria
1. **Capacity Invariant**: The aggregate weight $\sum_{p \in \mathcal{S}} w(p) \le W_{\max}$ and volume $\sum_{p \in \mathcal{S}} v(p) \le V_{\max}$.
2. **Tour Invariant**: The vehicle tour $\mathcal{T} = \langle v_0, v_{\pi(1)}, v_{\pi(2)}, \dots, v_{\pi(K)}, v_0 \rangle$ must begin and end at the Depot $v_0$ and visit every unique destination $\text{dest}(p)$ for all $p \in \mathcal{S}$ at least once.
3. **Optimality Invariant**: The DP packing solution must yield utility greater than or equal to any greedy discrete heuristic, and within the continuous upper bound established by Fractional Knapsack relaxation.

