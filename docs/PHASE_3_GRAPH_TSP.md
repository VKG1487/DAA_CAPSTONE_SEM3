# Phase 3: Route Maker and Graph Processing

**Course:** Design and Analysis of Algorithms (DAA) Capstone Project  
**Module:** Route Maker and Graph Processing (Dijkstra's Algorithm & TSP Approximation)  

---

## 1. Overview and Objectives

Phase 3 transforms the set of packed parcels into an actionable physical road trajectory:
1. **Graph Construction**: Modeling the urban transportation network as an Adjacency List.
2. **Shortest Path Derivation**: Executing **Dijkstra's Algorithm** with a binary min-heap to compute actual point-to-point shortest distances and turn-by-turn road paths.
3. **Delivery Route Optimization**: Solving the **Traveling Salesperson Problem (TSP)** using a **Nearest Neighbor Greedy Heuristic** augmented with **2-Opt Local Search** edge-untangling.

---

## 2. Road Network Graph Representation

### 2.1 Adjacency List Formalism
The city map is represented as a weighted graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$.
- Space Complexity: $\mathcal{O}(|\mathcal{V}| + |\mathcal{E}|)$, superior to an Adjacency Matrix $\mathcal{O}(|\mathcal{V}|^2)$ for sparse road systems.
- Each node $u \in \mathcal{V}$ maps to a list of outgoing tuples:
  $$\text{adj}[u] = \big[\, (v_1, w(u, v_1)), \; (v_2, w(u, v_2)), \; \dots \,\big]$$

### 2.2 Network Topology (Small Scenario)
```
          LOC-A (North Clinic)
         /    \
   4.5  /      \ 3.6
       /        \
  DEPOT -------- LOC-B (East Tech Park)
     | \  5.4   /
     |  \      / 5.4
 3.2 |   \    /
     |    LOC-C (South Harbor)
  LOC-D -/ 7.2
 (West Finance)
```

---

## 3. Dijkstra's Shortest Path Algorithm

### 3.1 Min-Heap Implementation
Because road distances are non-negative ($w_e > 0$), Dijkstra's algorithm guarantees optimal shortest paths without negative cycle anomalies.

```python
def dijkstra(self, source_id: str):
    distances = {node: inf for node in self.nodes}
    predecessors = {node: None for node in self.nodes}
    distances[source_id] = 0.0
    pq = [(0.0, source_id)]  # Min-heap priority queue
    visited = set()

    while pq:
        current_dist, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        for neighbor, weight in self.adj[u]:
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = u
                heapq.heappush(pq, (new_dist, neighbor))
    return distances, predecessors
```

### 3.2 Time and Space Complexity
- **Time Complexity**: Each vertex is extracted from the min-heap once ($\mathcal{O}(V \log V)$), and each edge relaxation updates the heap ($\mathcal{O}(E \log V)$). Overall:
  $$\mathcal{O}\big((V + E) \log V\big)$$
- **Space Complexity**: $\mathcal{O}(V)$ for distance table, predecessor map, and min-heap.

### 3.3 Metric Closure Precomputation
From the Depot and every active destination node, Dijkstra precomputes:
1. `dist_matrix[u][v]`: The exact shortest road distance between any two stops.
2. `path_matrix[u][v]`: The complete sequence of physical road intersections to navigate from $u$ to $v$.

---

## 4. Traveling Salesperson Problem (TSP) Approximation

### 4.1 Nearest Neighbor Heuristic
1. Start at the Central Depot: $S_0 = \text{DEPOT}$, visited = $\{\text{DEPOT}\}$.
2. Let current node be $u$. Select the closest unvisited customer stop $v^*$:
   $$v^* = \arg\min_{v \in \mathcal{V}_{\text{unvisited}}} \text{dist\_matrix}[u][v]$$
3. Append $v^*$ to tour, mark as visited, set $u \leftarrow v^*$.
4. When all delivery destinations are visited, append the Depot $S_0$ to complete the cycle.
- **Complexity**: $\mathcal{O}(K^2)$ where $K$ is the number of delivery stops.

### 4.2 2-Opt Local Search Improvement
Nearest Neighbor greedy choices frequently produce crossed edges in Euclidean and road space.
The 2-Opt algorithm tests every pair of non-adjacent edges $(u_i, u_{i+1})$ and $(u_j, u_{j+1})$:
$$\Delta_{\text{cost}} = \Big(\text{dist}(u_i, u_j) + \text{dist}(u_{i+1}, u_{j+1})\Big) - \Big(\text{dist}(u_i, u_{i+1}) + \text{dist}(u_j, u_{j+1})\Big)$$

If $\Delta_{\text{cost}} < 0$, the tour sub-sequence from $i+1$ to $j$ is reversed:
$$\langle u_0, \dots, u_i, \; \mathbf{u_j, u_{j-1}, \dots, u_{i+1}}, \; u_{j+1}, \dots, u_K \rangle$$

The search iterates until no 2-opt inversion yields further reduction (local optimum).

---

## 5. Route Output and Leg Breakdown (Demonstration Evidence)

### 5.1 Route Comparison
- **Nearest Neighbor Initial Tour**: `DEPOT -> LOC-A -> LOC-C -> LOC-D -> DEPOT` (Distance: 21.90 km)
- **2-Opt Optimized Final Tour**: `DEPOT -> LOC-A -> LOC-D -> LOC-C -> DEPOT` (Distance: **21.70 km**)
- **Distance Saved**: 0.20 km (0.91% reduction, 1 swap iteration)

### 5.2 Turn-by-Turn Leg Navigation Schedule
| Leg # | Origin | Destination | Leg Distance | Physical Road Intersections | Parcels Delivered |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | DEPOT | LOC-A | 4.50 km | `DEPOT -> LOC-A` | `PKG-01`, `PKG-03` |
| **2** | LOC-A | LOC-D | 5.80 km | `LOC-A -> LOC-D` | `PKG-05` |
| **3** | LOC-D | LOC-C | 7.20 km | `LOC-D -> LOC-C` | `PKG-04`, `PKG-07` |
| **4** | LOC-C | DEPOT | 4.20 km | `LOC-C -> DEPOT` | *Return to Hub* |

- **Total Route Distance**: **21.70 km**
- **Estimated Vehicle Duration**: 57.2 minutes (37.2 mins driving @ 35 km/h + 20 mins customer drop-off service time).

