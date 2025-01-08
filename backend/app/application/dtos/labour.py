from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from app.application.dtos.announcement import AnnouncementDTO
from app.application.dtos.contraction import ContractionDTO
from app.application.dtos.labour_pattern import LabourPatternDTO
from app.domain.labour.entity import Labour


@dataclass
class LabourDTO:
    """Data Transfer Object for Labour aggregate"""

    id: str
    birthing_person_id: str
    start_time: datetime
    end_time: datetime | None
    current_phase: str
    notes: str | None
    contractions: list[ContractionDTO]
    announcements: list[AnnouncementDTO]
    pattern: LabourPatternDTO | None

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        """Create DTO from domain aggregate"""
        contraction_pattern = labour.get_contraction_pattern()
        return cls(
            id=str(labour.id_.value),
            birthing_person_id=labour.birthing_person_id.value,
            start_time=labour.start_time,
            end_time=labour.end_time,
            current_phase=labour.current_phase.value,
            notes=labour.notes,
            contractions=[ContractionDTO.from_domain(c) for c in labour.contractions],
            announcements=[AnnouncementDTO.from_domain(a) for a in labour.announcements],
            pattern=LabourPatternDTO.from_domain(contraction_pattern)
            if contraction_pattern
            else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "birthing_person_id": self.birthing_person_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "current_phase": self.current_phase,
            "notes": self.notes,
            "contractions": [c.to_dict() for c in self.contractions],
            "announcements": [a.to_dict() for a in self.announcements],
            "pattern": self.pattern.to_dict() if self.pattern else None,
        }
