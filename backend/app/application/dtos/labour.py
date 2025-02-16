from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from app.application.dtos.labour_update import LabourUpdateDTO
from app.application.dtos.contraction import ContractionDTO
from app.application.dtos.labour_statistics import LabourStatisticsDTO
from app.domain.labour.entity import Labour
from app.domain.services.should_call_midwife_urgently import ShouldCallMidwifeUrgentlyService
from app.domain.services.should_go_to_hospital import ShouldGoToHospitalService


@dataclass
class LabourDTO:
    """Data Transfer Object for Labour aggregate"""

    id: str
    birthing_person_id: str
    start_time: datetime
    end_time: datetime | None
    current_phase: str
    notes: str | None
    should_go_to_hospital: bool
    should_call_midwife_urgently: bool
    contractions: list[ContractionDTO]
    announcements: list[LabourUpdateDTO]
    status_updates: list[LabourUpdateDTO]
    statistics: LabourStatisticsDTO

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        """Create DTO from domain aggregate"""
        should_go_to_hospital = ShouldGoToHospitalService().should_go_to_hospital(labour)
        should_call_midwife_urgently = (
            ShouldCallMidwifeUrgentlyService().should_call_midwife_urgently(labour)
        )
        return cls(
            id=str(labour.id_.value),
            birthing_person_id=labour.birthing_person_id.value,
            start_time=labour.start_time,
            end_time=labour.end_time,
            current_phase=labour.current_phase.value,
            notes=labour.notes,
            should_go_to_hospital=should_go_to_hospital,
            should_call_midwife_urgently=should_call_midwife_urgently,
            contractions=[ContractionDTO.from_domain(c) for c in labour.contractions],
            announcements=[LabourUpdateDTO.from_domain(a) for a in labour.announcements],
            status_updates=[LabourUpdateDTO.from_domain(s) for s in labour.status_updates],
            statistics=LabourStatisticsDTO.from_contractions(labour.contractions),
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
            "should_go_to_hospital": self.should_go_to_hospital,
            "should_call_midwife_urgently": self.should_call_midwife_urgently,
            "contractions": [c.to_dict() for c in self.contractions],
            "announcements": [a.to_dict() for a in self.announcements],
            "status_updates": [s.to_dict() for s in self.status_updates],
            "statistics": self.statistics.to_dict(),
        }
