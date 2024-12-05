from abc import abstractmethod
from typing import Protocol

from app.domain.user.entity_user import User
from app.domain.user.vo_user import UserId, Username


class UserGatewayInterface(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def read_by_id(self, user_id: UserId) -> User | None:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def delete_by_id(self, user_id: UserId) -> bool:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def read_by_username(
        self, username: Username, for_update: bool = False
    ) -> User | None:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def is_username_unique(self, username: Username) -> bool:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def read_all(self, limit: int, offset: int) -> list[User]:
        """
        :raises GatewayError:
        """
