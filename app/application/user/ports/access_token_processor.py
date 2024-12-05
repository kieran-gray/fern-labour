from abc import abstractmethod
from typing import Protocol

from app.application.user.ports.session_timer import SessionTimerInterface


class AccessTokenProcessorInterface(Protocol):
    _session_timer: SessionTimerInterface

    @abstractmethod
    def issue_access_token(self, session_id: str) -> str: ...

    @abstractmethod
    def extract_session_id(self, access_token: str) -> str:
        """
        :raises AdapterError:
        """
