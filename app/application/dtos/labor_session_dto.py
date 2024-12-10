from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.dtos.contraction_dto import ContractionDTO
from app.application.dtos.labor_pattern_dto import LaborPatternDTO
from app.domain.entities.labor_session import LaborSession


@dataclass
class LaborSessionDTO:
    """Data Transfer Object for LaborSession aggregate"""

    id: UUID
    user_id: UUID
    start_time: datetime
    end_time: datetime | None
    current_phase: str
    hospital_notified: bool
    notes: str | None
    contractions: list[ContractionDTO]
    pattern: LaborPatternDTO | None

    @classmethod
    def from_domain(cls, session: LaborSession) -> "LaborSessionDTO":
        """Create DTO from domain aggregate"""
        return cls(
            id=session.id_.value,
            user_id=session.user_id,
            start_time=session.start_time,
            end_time=session.end_time,
            current_phase=session.current_phase.value,
            notes=session.notes,
            contractions=[ContractionDTO.from_domain(c) for c in session.contractions],
            pattern=LaborPatternDTO.from_domain(session.get_contraction_pattern()),
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "current_phase": self.current_phase,
            "hospital_notified": self.hospital_notified,
            "notes": self.notes,
            "contractions": [c.to_dict() for c in self.contractions],
            "pattern": self.pattern.to_dict() if self.pattern else None,
        }
