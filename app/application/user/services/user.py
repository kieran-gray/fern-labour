import logging
from uuid import UUID

from app.application.committer import CommitterInterface
from app.application.user.gateways.user import UserGatewayInterface
from app.application.user.ports.password_hasher import PasswordHasherInterface
from app.application.user.ports.user_id_generator import (
    UserIdGeneratorInterface,
)
from app.domain.user.entity_user import User
from app.domain.user.enums import UserRoleEnum
from app.domain.user.exceptions.existence import UsernameAlreadyExists
from app.domain.user.exceptions.non_existence import (
    UserNotFoundById,
    UserNotFoundByUsername,
)
from app.domain.user.vo_user import UserId, Username

log = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_gateway: UserGatewayInterface,
        user_id_generator: UserIdGeneratorInterface,
        password_hasher: PasswordHasherInterface,
        committer: CommitterInterface,
    ):
        self._user_gateway = user_gateway
        self._user_id_generator = user_id_generator
        self._password_hasher = password_hasher
        self._committer = committer

    async def check_username_uniqueness(self, username: Username) -> None:
        """
        :raises GatewayError:
        :raises UsernameAlreadyExists:
        """
        log.debug(f"Started. Username: '{username.value}'.")

        if not await self._user_gateway.is_username_unique(username):
            raise UsernameAlreadyExists(username.value)

        log.debug(f"Done. Username: '{username.value}'.")

    async def create_user(self, username: Username, password: str) -> User:
        log.debug(f"Started. Username: '{username.value}'.")

        user_id: UUID = self._user_id_generator()
        password_hash: bytes = self._password_hasher.hash(password)
        user: User = User.create(
            user_id=user_id,
            username=username.value,
            password_hash=password_hash,
        )

        log.debug(f"Done. Username: '{username.value}'.")

        return user

    async def assign_roles(self, user: User, roles: set[UserRoleEnum]):
        """
        :raises GatewayError:
        """

        user.roles = roles
        user.roles.add(UserRoleEnum.USER)

        await self.save_user(user)

    async def save_user(self, user: User) -> None:
        """
        :raises GatewayError:
        """
        log.debug(f"Started. Username: '{user.username.value}'.")

        await self._user_gateway.save(user)

        await self._committer.commit()

        log.debug(
            "Save user: done. New user: '%s', '%s', '%s'.",
            user.id_.value,
            user.username.value,
            ", ".join(str(role.value) for role in user.roles),
        )

    async def get_all(self, limit: int, offset: int):
        """
        :raises GatewayError:
        """

        users = await self._user_gateway.read_all(limit=limit, offset=offset)

        return users

    async def get_user_by_username(self, username: Username) -> User:
        """
        :raises GatewayError:
        :raises UserNotFoundByUsername:
        """
        log.debug(f"Started. Username: '{username.value}'.")

        user: User | None = await self._user_gateway.read_by_username(username)
        if user is None:
            raise UserNotFoundByUsername(username.value)

        log.debug(f"Done. Username: '{username.value}'.")
        return user

    async def get_user_by_id(self, user_id: UserId) -> User:
        """
        :raises GatewayError:
        :raises UserNotFoundById:
        """
        log.debug(f"Started. User id: '{user_id.value}'.")

        user: User | None = await self._user_gateway.read_by_id(user_id)
        if user is None:
            raise UserNotFoundById(user_id)

        log.debug(f"Done. Username: '{user_id.value}'.")
        return user

    async def delete_user_by_id(self, user_id: UserId) -> User:
        """
        :raises GatewayError:
        :raises UserNotFoundById:
        """
        log.debug(f"Started. User id: '{user_id.value}'.")

        user: bool = await self._user_gateway.delete_by_id(user_id)
        if user is None:
            raise UserNotFoundById(user_id)

        await self._committer.commit()

        log.debug(f"Done. Username: '{user_id.value}'.")
        return user
