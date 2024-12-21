from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID

from app.application.dtos.contraction import ContractionDTO
from app.application.dtos.labour_pattern import LabourPatternDTO
from app.domain.labour.entity import Labour


@dataclass
class LabourDTO:
    """Data Transfer Object for Labour aggregate"""

    id: str
    birthing_person_id: UUID
    start_time: datetime
    end_time: datetime | None
    current_phase: str
    notes: str | None
    contractions: list[ContractionDTO]
    pattern: LabourPatternDTO | None

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        """Create DTO from domain aggregate"""
        contraction_pattern = labour.get_contraction_pattern()
        return cls(
            id=labour.id_.value,
            birthing_person_id=labour.birthing_person_id,
            start_time=labour.start_time,
            end_time=labour.end_time,
            current_phase=labour.current_phase.value,
            notes=labour.notes,
            contractions=[ContractionDTO.from_domain(c) for c in labour.contractions],
            pattern=LabourPatternDTO.from_domain(contraction_pattern)
            if contraction_pattern
            else None,
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "birthing_person_id": str(self.birthing_person_id),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "current_phase": self.current_phase,
            "notes": self.notes,
            "contractions": [c.to_dict() for c in self.contractions],
            "pattern": self.pattern.to_dict() if self.pattern else None,
        }
