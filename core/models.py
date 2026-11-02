"""
Data Models for Courier Problem Planning System
Phase 1: Problem Definition & Data Structures
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


PRIORITY_WEIGHTS = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}


@dataclass
class Parcel:
    """Represents a parcel to be evaluated, prioritized, packed, and delivered."""
    id: str
    destination_id: str
    priority: str          # "Critical", "High", "Medium", "Low"
    deadline_hours: float   # Target delivery window from departure (in hours)
    weight: float          # In kilograms (kg)
    volume: float          # In liters (L) or cubic decimeters
    value: float           # Delivery utility score / revenue value (points or $)
    description: str = ""

    @property
    def priority_level(self) -> int:
        """Numerical priority level (1 to 4)."""
        return PRIORITY_WEIGHTS.get(self.priority, 1)

    @property
    def composite_score(self) -> float:
        """
        Calculates an integrated prioritization score.
        Higher priority level, earlier deadline (1 / (deadline + 1)), and higher value
        yield a higher score.
        """
        urgency_term = 10.0 / (self.deadline_hours + 0.5)
        priority_term = self.priority_level * 5.0
        value_density = self.value / max(self.weight, 0.1)
        return round(urgency_term + priority_term + value_density, 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "priority": self.priority,
            "deadline_hours": self.deadline_hours,
            "weight": self.weight,
            "volume": self.volume,
            "value": self.value,
            "composite_score": self.composite_score,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Parcel":
        return cls(
            id=str(data["id"]),
            destination_id=str(data["destination_id"]),
            priority=str(data.get("priority", "Medium")),
            deadline_hours=float(data.get("deadline_hours", 4.0)),
            weight=float(data.get("weight", 1.0)),
            volume=float(data.get("volume", 1.0)),
            value=float(data.get("value", 10.0)),
            description=str(data.get("description", ""))
        )


@dataclass
class DeliveryPoint:
    """Represents a geographical delivery node (Depot or customer address)."""
    id: str
    name: str
    x: float
    y: float
    is_depot: bool = False
    service_time_mins: float = 5.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "is_depot": self.is_depot,
            "service_time_mins": self.service_time_mins
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeliveryPoint":
        return cls(
            id=str(data["id"]),
            name=str(data.get("name", data["id"])),
            x=float(data.get("x", 0.0)),
            y=float(data.get("y", 0.0)),
            is_depot=bool(data.get("is_depot", False)),
            service_time_mins=float(data.get("service_time_mins", 5.0))
        )


@dataclass
class RoadEdge:
    """Represents a road connecting two nodes with physical distance (km)."""
    source: str
    destination: str
    distance: float
    bidirectional: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "destination": self.destination,
            "distance": self.distance,
            "bidirectional": self.bidirectional
        }


@dataclass
class DeliveryTrip:
    """Comprehensive plan for one delivery vehicle dispatch trip."""
    selected_parcels: List[Parcel] = field(default_factory=list)
    unselected_parcels: List[Parcel] = field(default_factory=list)
    route_sequence: List[str] = field(default_factory=list)  # e.g., ["DEPOT", "LOC-A", "LOC-C", "DEPOT"]
    detailed_legs: List[Dict[str, Any]] = field(default_factory=list)
    total_distance_km: float = 0.0
    total_weight_kg: float = 0.0
    total_volume_l: float = 0.0
    total_value: float = 0.0
    weight_capacity_kg: float = 0.0
    volume_capacity_l: float = 0.0
    dp_matrix: Optional[List[List[float]]] = None

