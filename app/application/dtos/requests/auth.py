import re

from pydantic import BaseModel, field_validator

from app.domain.constants.user import PATTERN_EMAIL


def email_validator(value) -> None:
    if not re.fullmatch(PATTERN_EMAIL, value):
        raise ValueError(f"Username {value} is not a valid email address")


class LogInRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def username_must_be_a_valid_email(cls, value) -> str:
        email_validator(value)
        return value


class SignUpRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def username_must_be_a_valid_email(cls, value) -> str:
        email_validator(value)
        return value
