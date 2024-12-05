from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.user.constants import (
    PASSWORD_MIN_LEN,
    USERNAME_MAX_LEN,
    USERNAME_MIN_LEN,
)
from app.presentation.user.request_schemas_validation.username import (
    validate_username,
)


class LogInRequestPydantic(BaseModel):
    model_config = ConfigDict(frozen=True)

    username: str = Field(
        min_length=USERNAME_MIN_LEN,
        max_length=USERNAME_MAX_LEN,
        description=f"Username must be between "
        f"{USERNAME_MIN_LEN} and "
        f"{USERNAME_MAX_LEN} characters.",
    )
    password: str = Field(
        min_length=PASSWORD_MIN_LEN,
        description=f"Password must be at least {PASSWORD_MIN_LEN} characters long.",
    )

    @field_validator("username")
    @classmethod
    def _validate_username(cls, value: str) -> str:
        return validate_username(value)


@dataclass(frozen=True, slots=True)
class LogInResponse:
    message: str
