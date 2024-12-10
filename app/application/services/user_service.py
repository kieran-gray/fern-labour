import logging

from app.application.adapters.password_hasher import PasswordHasher
from app.domain.entities.user import User, UserRoleEnum
from app.domain.exceptions.user import (
    UsernameAlreadyExists,
    UserNotFoundById,
    UserNotFoundByUsername,
)
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.user_username import Username

log = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def check_username_uniqueness(self, username: Username) -> None:
        if await self._user_repository.email_exists(username):
            raise UsernameAlreadyExists(username.value)

    async def create_user(self, username: Username, password: str) -> User:
        password_hash: bytes = self._password_hasher.hash(password)
        user: User = User.create(
            username=username.value,
            password_hash=password_hash,
        )
        return user

    async def assign_roles(self, user: User, roles: set[UserRoleEnum]) -> None:
        user.roles = roles
        user.roles.add(UserRoleEnum.USER)
        await self._user_repository.save(user)

    async def save_user(self, user: User) -> None:
        await self._user_repository.save(user)

    async def get_user_by_username(self, username: Username) -> User:
        user: User | None = await self._user_repository.get_by_email(username.value)
        if user is None:
            raise UserNotFoundByUsername(username.value)

        return user

    async def get_user_by_id(self, user_id: UserId) -> User:
        user: User | None = await self._user_repository.get_by_id(user_id.value)
        if user is None:
            raise UserNotFoundById(user_id)

        return user

    async def delete_user_by_id(self, user_id: UserId) -> User:
        await self._user_repository.delete(user_id)
