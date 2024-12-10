from typing import Any

from app.domain.base.exceptions import DomainError, DomainValidationError
from app.domain.constants.user import USERNAME_MAX_LEN, USERNAME_MIN_LEN


class UsernameAlreadyExists(DomainError):
    def __init__(self, username: Any):
        super().__init__(f"User with username '{username}' already exists.")


class UserNotFoundById(DomainError):
    def __init__(self, user_id: Any):
        super().__init__(f"User with id '{user_id}' is not found.")


class UserNotFoundByUsername(DomainError):
    def __init__(self, username: Any):
        super().__init__(f"User with username '{username}' is not found.")


class UsernameInvalid(DomainValidationError):
    def __init__(self, username: str):
        super().__init__(f"Username {username} is not a valid email address")


class UsernameTooShort(DomainValidationError):
    def __init__(self, username: str):
        super().__init__(f"Username {username} is not a valid email address")


class UsernameTooLong(DomainValidationError):
    def __init__(self, username: str):
        super().__init__(f"Username {username} is not a valid email address")

        if not len(self.value) >= USERNAME_MIN_LEN:
            raise DomainValidationError(
                f"Username length must be greater or equal to {USERNAME_MIN_LEN} characters"
            )

        if not len(self.value) <= USERNAME_MAX_LEN:
            raise DomainValidationError(
                f"Username must be less than or equal to {USERNAME_MAX_LEN} characters"
            )
