from typing import Any

from app.common.domain.exceptions import DomainError


class UserNotFoundById(DomainError):
    def __init__(self, user_id: Any) -> None:
        super().__init__(f"User with id '{user_id}' is not found.")


class UserHasActiveLabour(DomainError):
    def __init__(self, user_id: Any) -> None:
        super().__init__(f"User with id '{user_id}' already has an active labour")


class UserDoesNotHaveActiveLabour(DomainError):
    def __init__(self, user_id: Any) -> None:
        super().__init__(f"User with id '{user_id}' does not have an active labour")


class UserCannotSubscribeToSelf(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot subscribe to self")
