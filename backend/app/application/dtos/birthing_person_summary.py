from dataclasses import dataclass
from typing import Any, Self

from app.domain.birthing_person.entity import BirthingPerson


@dataclass
class BirthingPersonSummaryDTO:
    """Data Transfer Object for Birthing Person Summary"""

    id: str
    first_name: str
    last_name: str

    @classmethod
    def from_domain(cls, birthing_person: BirthingPerson) -> Self:
        """Create DTO from domain"""
        return cls(
            id=birthing_person.id_.value,
            first_name=birthing_person.first_name,
            last_name=birthing_person.last_name,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
