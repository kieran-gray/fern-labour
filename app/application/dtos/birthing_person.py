from dataclasses import dataclass
from typing import Any, Self

from app.application.dtos.labour import LabourDTO
from app.domain.birthing_person.entity import BirthingPerson


@dataclass
class BirthingPersonDTO:
    """Data Transfer Object for Birthing Person aggregate"""

    id: str
    first_name: str
    last_name: str
    labours: list[LabourDTO]
    subscribers: list[str]

    @classmethod
    def from_domain(cls, birthing_person: BirthingPerson) -> Self:
        """Create DTO from domain aggregate"""
        return cls(
            id=birthing_person.id_.value,
            first_name=birthing_person.first_name,
            last_name=birthing_person.last_name,
            labours=[LabourDTO.from_domain(labour) for labour in birthing_person.labours],
            subscribers=[subscriber_id.value for subscriber_id in birthing_person.subscribers],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "labours": [labour.to_dict() for labour in self.labours],
            "subscribers": self.subscribers,
        }
