from dataclasses import dataclass

from app.domain.user.enums import UserRoleEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserRequest:
    username: str
    password: str
    roles: set[UserRoleEnum]
