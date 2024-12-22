from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from app.domain.contraction.entity import Contraction


@dataclass
class ContractionDTO:
    """Data Transfer Object for Contraction entity"""

    id: str
    labour_id: str
    start_time: datetime
    end_time: datetime
    duration_minutes: float
    intensity: int | None
    notes: str | None
    is_active: bool

    @classmethod
    def from_domain(cls, contraction: Contraction) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=str(contraction.id_.value),
            labour_id=str(contraction.labour_id.value),
            start_time=contraction.start_time,
            end_time=contraction.end_time,
            duration_minutes=contraction.duration.duration_minutes,
            intensity=contraction.intensity,
            notes=contraction.notes,
            is_active=contraction.is_active,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "labour_id": self.labour_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "intensity": self.intensity,
            "notes": self.notes,
            "is_active": self.is_active,
        }
