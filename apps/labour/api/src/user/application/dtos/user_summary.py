from dataclasses import dataclass
from typing import Any, Self

from src.user.domain.entity import User


@dataclass
class UserSummaryDTO:
    """Summary Data Transfer Object for User entity"""

    id: str
    first_name: str
    last_name: str

    @classmethod
    def from_domain(cls, user: User) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=user.id_.value,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
