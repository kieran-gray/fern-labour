from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Self

from app.labour.application.dtos.contraction import ContractionDTO
from app.labour.application.dtos.labour_update import LabourUpdateDTO
from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.services.should_call_midwife_urgently import (
    ShouldCallMidwifeUrgentlyService,
)
from app.labour.domain.labour.services.should_go_to_hospital import ShouldGoToHospitalService
from app.labour.domain.labour.services.should_prepare_for_hospital import (
    ShouldPrepareForHospitalService,
)


class RecommendationType(StrEnum):
    PREPARE_FOR_HOSPITAL = "prepare_for_hospital"
    GO_TO_HOSPITAL = "go_to_hospital"
    CALL_MIDWIFE = "call_midwife"


RECOMMENDATION_TYPE_TO_FUNCTION = {
    RecommendationType.CALL_MIDWIFE: ShouldCallMidwifeUrgentlyService().should_call_midwife_urgently,  # noqa: E501
    RecommendationType.GO_TO_HOSPITAL: ShouldGoToHospitalService().should_go_to_hospital,
    RecommendationType.PREPARE_FOR_HOSPITAL: ShouldPrepareForHospitalService().should_prepare_for_hospital,  # noqa: E501
}


@dataclass
class LabourDTO:
    """Data Transfer Object for Labour aggregate"""

    id: str
    birthing_person_id: str
    current_phase: str
    due_date: datetime
    first_labour: bool
    labour_name: str | None
    payment_plan: str | None
    start_time: datetime | None
    end_time: datetime | None
    notes: str | None
    recommendations: dict[str, bool]
    contractions: list[ContractionDTO]
    announcements: list[LabourUpdateDTO]
    status_updates: list[LabourUpdateDTO]

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        """Create DTO from domain aggregate"""
        recommendations = {
            recommendation_type.value: RECOMMENDATION_TYPE_TO_FUNCTION[recommendation_type](labour)
            for recommendation_type in RecommendationType
        }
        return cls(
            id=str(labour.id_.value),
            birthing_person_id=labour.birthing_person_id.value,
            current_phase=labour.current_phase.value,
            due_date=labour.due_date,
            first_labour=labour.first_labour,
            labour_name=labour.labour_name,
            payment_plan=labour.payment_plan,
            start_time=labour.start_time,
            end_time=labour.end_time,
            notes=labour.notes,
            recommendations=recommendations,
            contractions=[ContractionDTO.from_domain(c) for c in labour.contractions],
            announcements=[LabourUpdateDTO.from_domain(a) for a in labour.announcements],
            status_updates=[LabourUpdateDTO.from_domain(s) for s in labour.status_updates],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "birthing_person_id": self.birthing_person_id,
            "current_phase": self.current_phase,
            "due_date": self.due_date.isoformat(),
            "first_labour": self.first_labour,
            "labour_name": self.labour_name,
            "payment_plan": self.payment_plan,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "notes": self.notes,
            "recommendations": self.recommendations,
            "contractions": [c.to_dict() for c in self.contractions],
            "announcements": [a.to_dict() for a in self.announcements],
            "status_updates": [s.to_dict() for s in self.status_updates],
        }
