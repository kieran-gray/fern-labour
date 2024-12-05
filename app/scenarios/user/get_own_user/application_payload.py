from dataclasses import dataclass

from app.domain.user.enums import UserRoleEnum


@dataclass(frozen=True, slots=True)
class GetOwnUserResponse:
    username: str
    roles: set[UserRoleEnum]
