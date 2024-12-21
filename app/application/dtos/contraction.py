from dataclasses import dataclass
from datetime import datetime
from typing import Self

from app.domain.contraction.entity import Contraction


@dataclass
class ContractionDTO:
    """Data Transfer Object for Contraction entity"""

    id: str
    labour_id: str
    start_time: datetime
    end_time: datetime
    duration_minutes: float
    intensity: int
    notes: str | None
    is_active: bool

    @classmethod
    def from_domain(cls, contraction: Contraction) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=contraction.id_.value,
            labour_id=contraction.labour_id,
            start_time=contraction.start_time,
            end_time=contraction.end_time,
            duration_minutes=contraction.duration.duration_minutes,
            intensity=contraction.intensity,
            notes=contraction.notes,
            is_active=contraction.is_active,
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "labour_id": str(self.labour_id),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "intensity": self.intensity,
            "notes": self.notes,
            "is_active": self.is_active,
        }
