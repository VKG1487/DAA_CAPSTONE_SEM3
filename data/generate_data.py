"""
Utility to generate medium, large, and sample CSV datasets for the Courier Planning System.
"""

import json
import random
import csv
import math

def generate_datasets():
    random.seed(42)  # Deterministic seed for reproducible academic grading

    # 1. Medium Dataset: 12 nodes, 25 parcels
    medium_nodes = [
        {"id": "DEPOT", "name": "Central Hub", "x": 0.0, "y": 0.0, "is_depot": True, "service_time_mins": 0.0},
        {"id": "LOC-01", "name": "Airport Logistics", "x": 8.0, "y": 6.0, "is_depot": False, "service_time_mins": 5.0},
        {"id": "LOC-02", "name": "Metro General Hospital", "x": -4.0, "y": 7.0, "is_depot": False, "service_time_mins": 6.0},
        {"id": "LOC-03", "name": "Downtown Shopping Complex", "x": 3.0, "y": -5.0, "is_depot": False, "service_time_mins": 4.0},
        {"id": "LOC-04", "name": "Suburban Residential North", "x": -2.0, "y": 10.0, "is_depot": False, "service_time_mins": 5.0},
        {"id": "LOC-05", "name": "Industrial Sector East", "x": 10.0, "y": 1.0, "is_depot": False, "service_time_mins": 7.0},
        {"id": "LOC-06", "name": "South Port Terminal", "x": 1.0, "y": -9.0, "is_depot": False, "service_time_mins": 8.0},
        {"id": "LOC-07", "name": "University Campus", "x": -7.0, "y": -3.0, "is_depot": False, "service_time_mins": 4.0},
        {"id": "LOC-08", "name": "Financial District", "x": 2.0, "y": 3.0, "is_depot": False, "service_time_mins": 4.0},
        {"id": "LOC-09", "name": "West Residential Suburb", "x": -9.0, "y": 4.0, "is_depot": False, "service_time_mins": 5.0},
        {"id": "LOC-10", "name": "Technology Corridor", "x": 6.0, "y": -2.0, "is_depot": False, "service_time_mins": 5.0},
        {"id": "LOC-11", "name": "Northwest Clinic", "x": -5.0, "y": 2.0, "is_depot": False, "service_time_mins": 4.0}
    ]

    # Generate road edges for medium nodes
    medium_edges = []
    for i in range(len(medium_nodes)):
        u = medium_nodes[i]
        for j in range(i + 1, len(medium_nodes)):
            v = medium_nodes[j]
            dist = math.sqrt((u["x"] - v["x"])**2 + (u["y"] - v["y"])**2)
            # Add edge if close enough to maintain realistic sparse planar road topology
            if dist <= 11.0:
                road_distance = round(dist * random.uniform(1.1, 1.25), 1)
                medium_edges.append({
                    "source": u["id"],
                    "destination": v["id"],
                    "distance": road_distance,
                    "bidirectional": True
                })

    priorities = ["Critical", "High", "Medium", "Low"]
    customer_ids_medium = [n["id"] for n in medium_nodes if not n["is_depot"]]

    medium_parcels = []
    descriptions = [
        "Medical Diagnostic Kit", "Server Motherboard", "Urgent Legal Documents",
        "Laboratory Specimens", "Automotive ECU Module", "High-End Camera Lens",
        "Biotech Vaccines", "Corporate Laptops", "Architecture Blueprints",
        "Pharmaceutical Supplies", "Precision CNC Tooling", "Telecom Router",
        "Emergency Cardiac Monitor", "Optical Fiber Spool", "Designer Apparel",
        "Industrial Bearings", "Audit Dossier", "Retail Consumer Goods",
        "Solar Inverter Controller", "Hospital Sanitizer Batch", "Lithium Battery Pack",
        "Security Firewall Device", "Satellite Transceiver", "Specialty Chemistry Samples",
        "E-Commerce Express Delivery"
    ]

    for i in range(25):
        p_prio = random.choices(priorities, weights=[0.2, 0.35, 0.3, 0.15])[0]
        if p_prio == "Critical":
            deadline = round(random.uniform(1.0, 2.5), 1)
            val = round(random.uniform(60, 100), 1)
        elif p_prio == "High":
            deadline = round(random.uniform(2.5, 4.5), 1)
            val = round(random.uniform(40, 75), 1)
        elif p_prio == "Medium":
            deadline = round(random.uniform(4.0, 8.0), 1)
            val = round(random.uniform(20, 45), 1)
        else:
            deadline = round(random.uniform(7.0, 12.0), 1)
            val = round(random.uniform(10, 25), 1)

        weight = round(random.uniform(1.0, 7.0), 1)
        volume = round(weight * random.uniform(1.5, 3.0), 1)
        dest = random.choice(customer_ids_medium)

        medium_parcels.append({
            "id": f"PKG-{i+1:02d}",
            "destination_id": dest,
            "priority": p_prio,
            "deadline_hours": deadline,
            "weight": weight,
            "volume": volume,
            "value": val,
            "description": descriptions[i]
        })

    medium_dataset = {
        "name": "Medium City Courier Scenario",
        "description": "25 prioritized packages across 12 delivery points in a metropolitan distribution network.",
        "depot_id": "DEPOT",
        "truck_weight_capacity_kg": 40.0,
        "truck_volume_capacity_l": 120.0,
        "nodes": medium_nodes,
        "edges": medium_edges,
        "parcels": medium_parcels
    }

    with open("data/medium_dataset.json", "w", encoding="utf-8") as f:
        json.dump(medium_dataset, f, indent=2)

    # 2. Large Dataset: 35 nodes, 100 parcels
    large_nodes = [
        {"id": "DEPOT", "name": "Central Superhub", "x": 0.0, "y": 0.0, "is_depot": True, "service_time_mins": 0.0}
    ]
    for i in range(1, 35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(2.0, 20.0)
        large_nodes.append({
            "id": f"ZONE-{i:02d}",
            "name": f"Metropolitan Sector {i}",
            "x": round(radius * math.cos(angle), 1),
            "y": round(radius * math.sin(angle), 1),
            "is_depot": False,
            "service_time_mins": round(random.uniform(3.0, 6.0), 1)
        })

    large_edges = []
    for i in range(len(large_nodes)):
        u = large_nodes[i]
        for j in range(i + 1, len(large_nodes)):
            v = large_nodes[j]
            dist = math.sqrt((u["x"] - v["x"])**2 + (u["y"] - v["y"])**2)
            if dist <= 12.0:
                road_dist = round(dist * random.uniform(1.1, 1.3), 1)
                large_edges.append({
                    "source": u["id"],
                    "destination": v["id"],
                    "distance": road_dist,
                    "bidirectional": True
                })

    customer_ids_large = [n["id"] for n in large_nodes if not n["is_depot"]]
    large_parcels = []
    for i in range(100):
        p_prio = random.choices(priorities, weights=[0.25, 0.35, 0.25, 0.15])[0]
        if p_prio == "Critical":
            deadline = round(random.uniform(1.0, 2.5), 1)
            val = round(random.uniform(70, 120), 1)
        elif p_prio == "High":
            deadline = round(random.uniform(2.5, 5.0), 1)
            val = round(random.uniform(40, 80), 1)
        elif p_prio == "Medium":
            deadline = round(random.uniform(4.5, 9.0), 1)
            val = round(random.uniform(20, 50), 1)
        else:
            deadline = round(random.uniform(8.0, 16.0), 1)
            val = round(random.uniform(10, 30), 1)

        weight = round(random.uniform(0.8, 8.5), 1)
        volume = round(weight * random.uniform(1.5, 3.2), 1)
        dest = random.choice(customer_ids_large)

        large_parcels.append({
            "id": f"PKG-{i+1:03d}",
            "destination_id": dest,
            "priority": p_prio,
            "deadline_hours": deadline,
            "weight": weight,
            "volume": volume,
            "value": val,
            "description": f"Standard Consignment Item {i+1}"
        })

    large_dataset = {
        "name": "Large Metropolitan Courier Scenario",
        "description": "100 prioritized packages across 35 delivery points for rigorous algorithmic scalability testing.",
        "depot_id": "DEPOT",
        "truck_weight_capacity_kg": 80.0,
        "truck_volume_capacity_l": 250.0,
        "nodes": large_nodes,
        "edges": large_edges,
        "parcels": large_parcels
    }

    with open("data/large_dataset.json", "w", encoding="utf-8") as f:
        json.dump(large_dataset, f, indent=2)

    # 3. Sample CSV for UI File Upload Demo
    with open("data/parcels_sample.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "destination_id", "priority", "deadline_hours", "weight", "volume", "value", "description"])
        for p in medium_parcels[:15]:
            writer.writerow([p["id"], p["destination_id"], p["priority"], p["deadline_hours"], p["weight"], p["volume"], p["value"], p["description"]])

    print("Successfully generated data/medium_dataset.json, data/large_dataset.json, and data/parcels_sample.csv")

if __name__ == "__main__":
    generate_datasets()
