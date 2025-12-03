from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Self

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.services.should_go_to_hospital import ShouldGoToHospitalService


@dataclass
class LabourSummaryDTO:
    """Data Transfer Object for Labour aggregate"""

    id: str
    duration: float
    contraction_count: int
    current_phase: str
    hospital_recommended: bool

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        """Create DTO from domain aggregate"""
        hospital_recommended = ShouldGoToHospitalService().should_go_to_hospital(labour)
        duration = (
            (datetime.now(UTC) - labour.start_time).total_seconds() / 3600
            if labour.start_time
            else 0.0
        )
        return cls(
            id=str(labour.id_.value),
            duration=duration,
            contraction_count=len(labour.contractions),
            current_phase=labour.current_phase.value,
            hospital_recommended=hospital_recommended,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "duration": self.duration,
            "contraction_count": self.contraction_count,
            "current_phase": self.current_phase,
            "hospital_recommended": self.hospital_recommended,
        }
