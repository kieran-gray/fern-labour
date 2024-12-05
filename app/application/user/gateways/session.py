from abc import abstractmethod
from typing import Protocol

from app.application.user.record_session import SessionRecord
from app.domain.user.vo_user import UserId


class SessionGatewayInterface(Protocol):
    @abstractmethod
    async def save(self, session_record: SessionRecord) -> None:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def read(
        self, session_id: str, for_update: bool = False
    ) -> SessionRecord | None:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def delete(self, session_id: str) -> bool:
        """
        :raises GatewayError:
        """

    @abstractmethod
    async def delete_all_for_user(self, user_id: UserId) -> None:
        """
        :raises GatewayError:
        """
