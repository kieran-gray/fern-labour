from dataclasses import dataclass

from app.application.enums import ResponseStatusEnum


@dataclass(frozen=True, slots=True)
class UserResponse:
    username: str
    status: ResponseStatusEnum
