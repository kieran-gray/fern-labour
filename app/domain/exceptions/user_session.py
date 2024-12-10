from typing import Any

from app.domain.base.exceptions import DomainError


class SessionNotFoundById(DomainError):
    def __init__(self, session_id: Any):
        super().__init__(f"Session with id '{session_id}' is not found.")
