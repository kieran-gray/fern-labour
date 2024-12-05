from typing import Any

from app.domain.base.exceptions import DomainError


class UsernameAlreadyExists(DomainError):
    def __init__(self, username: Any):
        message: str = f"User with username '{username}' already exists."
        super().__init__(message)
