from abc import abstractmethod
from typing import Protocol

from app.application.adapters.session_timer import SessionTimer


class AccessTokenProcessor(Protocol):
    _session_timer: SessionTimer

    @abstractmethod
    def issue_access_token(self, user_id: str, session_id: str) -> str: ...

    @abstractmethod
    def extract_ids(self, access_token: str) -> tuple[str, str]: ...
