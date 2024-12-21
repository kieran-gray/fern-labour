from dataclasses import dataclass
from datetime import datetime
from typing import Self

from app.application.dtos.labour_pattern import LabourPatternDTO
from app.domain.labour.entity import Labour


@dataclass
class LabourSummaryDTO:
    """Data Transfer Object for Labour aggregate"""

    id: str
    duration: float
    contraction_count: int
    current_phase: str
    hospital_recommended: bool
    pattern: LabourPatternDTO | None

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        """Create DTO from domain aggregate"""
        contraction_pattern = labour.get_contraction_pattern()
        return cls(
            id=labour.id_.value,
            duration=(datetime.now() - labour.start_time).total_seconds() / 3600,
            contraction_count=len(labour.contractions),
            current_phase=labour.current_phase.value,
            hospital_recommended=labour.should_go_to_hospital,
            pattern=LabourPatternDTO.from_domain(contraction_pattern)
            if contraction_pattern
            else None,
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "duration": self.duration,
            "contraction_count": self.contraction_count,
            "current_phase": self.current_phase,
            "hospital_recommended": self.hospital_recommended,
            "pattern": self.pattern.to_dict() if self.pattern else None,
        }
