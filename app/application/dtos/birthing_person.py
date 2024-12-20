from dataclasses import dataclass
from typing import Self
from uuid import UUID

from app.application.dtos.contact import ContactDTO
from app.application.dtos.labour import LabourDTO
from app.domain.birthing_person.entity import BirthingPerson


@dataclass
class BirthingPersonDTO:
    """Data Transfer Object for Birthing Person aggregate"""

    id: UUID
    name: str
    first_labour: bool
    labours: list[LabourDTO]
    contacts: list[ContactDTO]

    @classmethod
    def from_domain(cls, birthing_person: BirthingPerson) -> Self:
        """Create DTO from domain aggregate"""
        return cls(
            id=birthing_person.id_.value,
            name=birthing_person.name,
            first_labour=birthing_person.first_labour,
            labours=[LabourDTO.from_domain(labour) for labour in birthing_person.labours],
            contacts=[ContactDTO.from_domain(contact) for contact in birthing_person.contacts],
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "name": self.name,
            "first_labour": self.first_labour,
            "labours": [labour.to_dict() for labour in self.labours],
            "contractions": [contact.to_dict() for contact in self.contacts],
        }
