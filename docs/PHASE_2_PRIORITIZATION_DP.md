# Phase 2: Package Prioritization and Box Filling

**Course:** Design and Analysis of Algorithms (DAA) Capstone Project  
**Module:** Package Prioritization and Box Filling (Sorting & Dynamic Programming)  

---

## 1. Overview and Objectives

Phase 2 addresses two core logistical challenges:
1. **Prioritizing incoming parcels** using divide-and-conquer sorting algorithms to establish delivery order under customer SLAs and deadlines.
2. **Optimizing package selection (Box Filling)** into a vehicle with payload limit $W_{\max}$ using Dynamic Programming, guaranteeing maximum utility.

---

## 2. Parcel Prioritization via Sorting

### 2.1 Multi-Key Priority Formulation
Parcels are evaluated against multiple operational criteria:
- **Earliest Deadline First (EDF)**: Urgency based on remaining delivery window.
- **Priority Tier**: Four-level SLA hierarchy (`Critical` > `High` > `Medium` > `Low`).
- **Value Density**: Ratio of parcel worth or utility to weight ($u_i / w_i$).
- **Composite Score**: Integrates all three dimensions into a scalar metric:
  $$\text{Composite}(p_i) = \frac{10}{T_{\text{due}} + 0.5} + 5 \cdot \text{PriorityWeight}(p_i) + \frac{u_i}{\max(w_i, 0.1)}$$

### 2.2 Algorithm Implementations from Scratch

#### 1. MergeSort Implementation (Divide and Conquer)
- **Recurrence**: $T(N) = 2T(N/2) + \Theta(N) \implies \Theta(N \log N)$ by the Master Theorem.
- **Properties**: Stable sorting algorithm; preserves relative order of packages with identical deadlines.
- **Auxiliary Space**: $\mathcal{O}(N)$ for auxiliary merging buffers.

#### 2. QuickSort Implementation (Partitioning)
- **Pivot Strategy**: Median-of-Three pivot selection ($\text{median}(\text{low}, \text{mid}, \text{high})$) to avoid worst-case $\mathcal{O}(N^2)$ degradation on pre-sorted arrays.
- **Properties**: In-place partitioning; average runtime $\mathcal{O}(N \log N)$; auxiliary stack space $\mathcal{O}(\log N)$.

#### 3. Empirical Sorting Comparison (Small Dataset: 8 Parcels)
| Sorting Algorithm | Execution Time (ms) | Element Comparisons | Space Complexity | Stability |
| :--- | :--- | :--- | :--- | :--- |
| **MergeSort (Scratch)** | 0.0581 ms | 15 comparisons | $\mathcal{O}(N)$ | Stable |
| **QuickSort (Median-of-3)** | 0.0512 ms | 22 comparisons | $\mathcal{O}(\log N)$ | Unstable |
| **Python TimSort** | 0.0117 ms | N/A (C implementation) | $\mathcal{O}(N)$ | Stable |

---

## 3. Dynamic Programming 0/1 Knapsack Solution

### 3.1 Mathematical Formulation
Let candidate parcels be indexed $i = 1, 2, \dots, N$. Each parcel has integer weight $w_i \in \mathbb{Z}^+$ (after scale discretization) and utility value $v_i \ge 0$.
The vehicle capacity is $W \in \mathbb{Z}^+$.

We define the subproblem state:
$$DP[i][w] = \text{Maximum value attainable using a subset of items } \{1, \dots, i\} \text{ with total weight } \le w.$$

#### Base Cases:
$$DP[0][w] = 0 \quad \forall \; 0 \le w \le W$$
$$DP[i][0] = 0 \quad \forall \; 0 \le i \le N$$

#### Bellman Recurrence Equation:
$$DP[i][w] = \begin{cases}
DP[i-1][w] & \text{if } w < w_i \\
\max\Big(DP[i-1][w], \; DP[i-1][w - w_i] + v_i\Big) & \text{if } w \ge w_i
\end{cases}$$

### 3.2 Step-by-Step DP Matrix Trace (Academic Demonstration Instance)
Consider the first items from the small dataset evaluated with capacity $W = 15.0$ kg:

| Item $i$ | Parcel ID | Destination | Weight $w_i$ | Value $v_i$ |
| :---: | :---: | :---: | :---: | :---: |
| 1 | PKG-05 | LOC-D | 2.0 kg | 51.67 |
| 2 | PKG-01 | LOC-A | 3.0 kg | 40.00 |
| 3 | PKG-04 | LOC-C | 5.0 kg | 26.73 |
| 4 | PKG-02 | LOC-B | 4.0 kg | 26.61 |
| 5 | PKG-03 | LOC-A | 2.0 kg | 20.82 |
| 6 | PKG-07 | LOC-C | 3.0 kg | 20.22 |
| 7 | PKG-08 | LOC-D | 4.0 kg | 14.33 |
| 8 | PKG-06 | LOC-B | 6.0 kg | 8.68 |

#### Dynamic Programming Table Output Slice:
```
Weight (kg) ->   0.0kg  2.0kg  4.0kg  6.0kg   8.0kg  10.0kg  12.0kg  14.0kg  15.0kg
-----------------------------------------------------------------------------------
Base (0 items)    0.00   0.00   0.00   0.00    0.00    0.00    0.00    0.00    0.00
PKG-05 (2.0kg)    0.00  51.67  51.67  51.67   51.67   51.67   51.67   51.67   51.67
PKG-01 (3.0kg)    0.00  51.67  51.67  91.67   91.67   91.67   91.67   91.67   91.67
PKG-04 (5.0kg)    0.00  51.67  51.67  91.67   91.67  118.40  118.40  118.40  118.40
PKG-02 (4.0kg)    0.00  51.67  51.67  91.67   91.67  118.40  118.40  145.01  145.01
PKG-03 (2.0kg)    0.00  51.67  72.49  91.67  112.49  118.40  139.22  145.01  145.01
PKG-07 (3.0kg)    0.00  51.67  72.49  91.67  112.49  132.71  139.22  159.32  159.44
PKG-08 (4.0kg)    0.00  51.67  72.49  91.67  112.49  132.71  139.22  159.32  159.44
PKG-06 (6.0kg)    0.00  51.67  72.49  91.67  112.49  132.71  139.22  159.32  159.44
```

### 3.3 Backtracking Item Reconstruction
To identify the selected items:
1. Start at cell $(i = N, w = W) = (8, 15)$.
2. If $DP[i][w] == DP[i-1][w]$, item $i$ was **not** selected $\implies i \leftarrow i - 1$.
3. If $DP[i][w] \neq DP[i-1][w]$, item $i$ was **selected** $\implies$ add item $i$ to manifest, $w \leftarrow w - w_i$, $i \leftarrow i - 1$.

#### Reconstruction Result:
- **Selected Parcels**: `PKG-05` (2 kg), `PKG-01` (3 kg), `PKG-04` (5 kg), `PKG-03` (2 kg), `PKG-07` (3 kg).
- **Total Payload Weight**: $2 + 3 + 5 + 2 + 3 = 15.0$ kg (**100.0% Capacity Utilization**).
- **Total Value**: **159.44 points**.
- **Deferred Parcels**: `PKG-02`, `PKG-08`, `PKG-06` (queued for Trip #2).

---

## 4. Theoretical Comparison: 0/1 Integer DP vs. Fractional Greedy Bound

| Property | 0/1 Knapsack (Integer DP) | Fractional Knapsack (Greedy Relaxation) |
| :--- | :--- | :--- |
| **Indivisibility** | Parcels cannot be cut ($x_i \in \{0, 1\}$) | Parcels can be fractioned ($x_i \in [0, 1]$) |
| **Algorithm** | Dynamic Programming | Greedy (sort by $v_i / w_i$) |
| **Optimal Value** | **159.44** | **164.66** |
| **Optimality Gap** | $\text{Exact Global Optimum}$ | $+3.17\%$ (Theoretical Upper Bound) |
| **Computational Class** | Pseudo-polynomial $\mathcal{O}(N \cdot W)$ | Polynomial $\mathcal{O}(N \log N)$ |

**Conclusion:** The greedy fractional relaxation proves that no discrete combination can ever exceed $164.66$. Our DP solution achieves $159.44$, which is the exact integer optimum.

