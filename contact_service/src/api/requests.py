import re
from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel

EMAIL_MAX_LENGTH = 254
EMAIL_REGEX = re.compile(r"^[\w\-+\.]+@([\w\-]+\.)+[\w\-]{2,4}$")

MESSAGE_MAX_LENGTH = 5000
NAME_MAX_LENGTH = 100


def email_validator(email: str) -> str:
    if len(email) > EMAIL_MAX_LENGTH or not EMAIL_REGEX.match(email):
        raise ValueError(f"{email} is not a valid email.")
    return email


def message_validator(message: str) -> str:
    if len(message) > MESSAGE_MAX_LENGTH:
        raise ValueError(f"Contact message exceeds max length of {MESSAGE_MAX_LENGTH} characters")
    return message


def name_validator(name: str) -> str:
    if len(name) > NAME_MAX_LENGTH:
        raise ValueError(f"Name exceeds max length of {NAME_MAX_LENGTH} characters")
    return name


class ContactUsRequest(BaseModel):
    category: str
    email: Annotated[str, AfterValidator(email_validator)]
    name: Annotated[str, AfterValidator(name_validator)]
    message: Annotated[str, AfterValidator(message_validator)]
    token: str
    data: dict[str, Any] | None = None
    user_id: str | None = None
