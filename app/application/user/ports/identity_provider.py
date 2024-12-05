from abc import abstractmethod
from typing import Protocol

from app.application.user.record_session import SessionRecord
from app.domain.user.enums import UserRoleEnum
from app.domain.user.vo_user import UserId


class IdentityProviderInterface(Protocol):
    @abstractmethod
    async def get_current_session(self) -> SessionRecord:
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
