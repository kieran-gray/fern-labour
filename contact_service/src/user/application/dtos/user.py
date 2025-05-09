from dataclasses import dataclass
from typing import Any, Self

from src.user.application.dtos.user_summary import UserSummaryDTO
from src.user.domain.entity import User


@dataclass
class UserDTO:
    """Data Transfer Object for User entity"""

    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str | None

    @classmethod
    def from_domain(cls, user: User) -> Self:
        """Create DTO from domain entity"""
        return cls(
            id=user.id_.value,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
        }

    def to_summary(self) -> UserSummaryDTO:
        return UserSummaryDTO(id=self.id, first_name=self.first_name, last_name=self.last_name)
