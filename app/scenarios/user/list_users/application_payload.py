from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.pagination import PaginationRequest
from app.domain.user.entity_user import User
from app.domain.user.enums import UserRoleEnum


@dataclass(frozen=True)
class ListUsersRequest(PaginationRequest):
    __slots__ = ()


@dataclass(frozen=True, slots=True)
class ListUsersResponseElement:
    id: UUID
    username: str
    roles: set[UserRoleEnum]
    is_active: bool

    @classmethod
    def from_user(cls, user: User) -> ListUsersResponseElement:
        return ListUsersResponseElement(
            user.id_.value,
            user.username.value,
            user.roles,
            user.is_active,
        )


@dataclass(frozen=True, slots=True)
class ListUsersResponse:
    users: list[ListUsersResponseElement]
