from typing import Any

from fern_labour_core.exceptions.domain import DomainError


class UserNotFoundById(DomainError):
    def __init__(self, user_id: Any) -> None:
        super().__init__(f"User with id '{user_id}' is not found.")
