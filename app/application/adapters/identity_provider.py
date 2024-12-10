from abc import abstractmethod
from typing import Protocol

from app.domain.entities.user import User, UserRoleEnum
from app.domain.entities.user_session import UserSession
from app.domain.value_objects.user_id import UserId


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user(self) -> User:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """

    @abstractmethod
    async def get_current_session(self) -> UserSession:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """

    @abstractmethod
    async def get_current_user_id(self) -> UserId:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        """

    @abstractmethod
    async def get_current_user_roles(self) -> set[UserRoleEnum]:
        """
        :raises AdapterError:
        :raises GatewayError:
        :raises SessionNotFoundById:
        :raises SessionExpired:
        :raises UserNotFoundById:
        """
