from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from app.domain.base.entity import Entity
from app.domain.entities.user_session import UserSession
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.user_password_hash import UserPasswordHash
from app.domain.value_objects.user_username import Username


class UserRoleEnum(StrEnum):
    ADMIN = "admin"
    USER = "user"


@dataclass(eq=False, kw_only=True)
class User(Entity[UserId]):
    username: Username
    password_hash: UserPasswordHash
    roles: set[UserRoleEnum] = field(default_factory=lambda: {UserRoleEnum.USER})
    is_active: bool
    sessions: list[UserSession] = field(default_factory=list)

    @classmethod
    def create(cls, *, username: str, password_hash: bytes, user_id: UUID | None = None) -> Self:
        return cls(
            id_=UserId(user_id or uuid4()),
            username=Username(username),
            password_hash=UserPasswordHash(password_hash),
            sessions=None,
            is_active=True,
        )

    def create_session(self, expiration: datetime, session_id: UUID | None = None) -> UserSession:
        session = UserSession(id_=session_id or uuid4(), user_id=self.id_, expiration=expiration)
        self.sessions.append(session)
        return session
    
    def delete_all_sessions(self) -> None:
        self.sessions = []

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def grant_admin(self) -> None:
        self.roles.add(UserRoleEnum.ADMIN)

    def revoke_admin(self) -> None:
        self.roles.discard(UserRoleEnum.ADMIN)
