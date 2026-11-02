"""
Generates clean, official, academic diagrams for Phase 1 (Architecture Workflow)
and Phase 2 (DP Table Heatmap/Matrix) to embed in the Word Report.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("output", exist_ok=True)

# 1. Architecture Flowchart (Classic, Official Monochrome/Navy Theme)
plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 4.2), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

boxes = [
    ("Candidate Parcels Pool\n(N Items with SLAs, Wt, Vol)", (1.2, 0.5)),
    ("Phase 2: Multi-Key Sorting\n(MergeSort / QuickSort)", (3.8, 0.5)),
    ("Phase 2: 0/1 Knapsack DP\n(Capacity W_max & V_max)", (6.4, 0.5)),
    ("Phase 3: Min-Heap Dijkstra\n(Road Metric Closure)", (9.0, 0.5)),
    ("Phase 3: TSP Tour & 2-Opt\n(Nearest Neighbor + Opt)", (11.6, 0.5)),
    ("Phase 5: Dispatch Order\n(Manifest & Turn Navigation)", (14.2, 0.5))
]

for title, (x, y) in boxes:
    ax.text(
        x, y, title,
        ha='center', va='center', fontsize=9, fontfamily='serif', fontweight='bold',
        bbox=dict(boxstyle="square,pad=0.6", facecolor='#F8F9FA', edgecolor='#2B3A42', lw=1.2)
    )

for i in range(len(boxes) - 1):
    x1 = boxes[i][1][0] + 1.1
    x2 = boxes[i+1][1][0] - 1.1
    ax.annotate(
        "", xy=(x2, 0.5), xytext=(x1, 0.5),
        arrowprops=dict(arrowstyle="-|>", color='#1B365D', lw=1.5, mutation_scale=12)
    )

ax.set_xlim(0, 15.5)
ax.set_ylim(0, 1.0)
ax.axis('off')
plt.title("Figure 1.1: Integrated Courier Planning System Algorithmic Architecture",
          fontsize=11, fontfamily='serif', fontweight='bold', color='#1A1A1A', pad=10)
plt.tight_layout()
plt.savefig("output/architecture_diagram.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. DP Matrix Visual Slice (Classic Table Heatmap)
fig, ax = plt.subplots(figsize=(9, 4.5), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Data from small dataset DP table
items = ["Base (0 items)", "PKG-05 (2kg)", "PKG-01 (3kg)", "PKG-04 (5kg)", "PKG-02 (4kg)", "PKG-03 (2kg)", "PKG-07 (3kg)"]
weights = [f"{w}kg" for w in [0, 2, 4, 6, 8, 10, 12, 14, 15]]

dp_matrix = [
    [0.0,   0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00],
    [0.0,  51.67, 51.67, 51.67, 51.67, 51.67, 51.67, 51.67, 51.67],
    [0.0,  51.67, 51.67, 91.67, 91.67, 91.67, 91.67, 91.67, 91.67],
    [0.0,  51.67, 51.67, 91.67, 91.67, 118.40, 118.40, 118.40, 118.40],
    [0.0,  51.67, 51.67, 91.67, 91.67, 118.40, 118.40, 145.01, 145.01],
    [0.0,  51.67, 72.49, 91.67, 112.49, 118.40, 139.22, 145.01, 145.01],
    [0.0,  51.67, 72.49, 91.67, 112.49, 132.71, 139.22, 159.32, 159.44],
]

cax = ax.matshow(dp_matrix, cmap='Blues', alpha=0.75)

for i in range(len(items)):
    for j in range(len(weights)):
        val = dp_matrix[i][j]
        txt = f"{val:.1f}" if val > 0 else "0"
        color = 'white' if val > 100 else 'black'
        ax.text(j, i, txt, ha='center', va='center', fontsize=8, fontfamily='serif', color=color)

ax.set_xticks(range(len(weights)))
ax.set_xticklabels(weights, fontsize=8, fontfamily='serif')
ax.set_yticks(range(len(items)))
ax.set_yticklabels(items, fontsize=8, fontfamily='serif')
ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

plt.title("Figure 2.1: Dynamic Programming 0/1 Knapsack Matrix State Evaluation (DP[i][w])",
          fontsize=10, fontfamily='serif', fontweight='bold', color='#1A1A1A', pad=20)
plt.xlabel("Vehicle Weight Capacity Increments (w)", fontsize=8, fontfamily='serif', labelpad=8)
plt.ylabel("Candidate Parcels Evaluated (i)", fontsize=8, fontfamily='serif')

plt.tight_layout()
plt.savefig("output/dp_table_visualization.png", dpi=300, bbox_inches='tight')
plt.close()

print("Architecture diagram and DP table visualization generated successfully.")
