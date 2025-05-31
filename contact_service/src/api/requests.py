import re
from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel, Field

EMAIL_MAX_LENGTH = 254
EMAIL_REGEX = re.compile(r"^[\w\-+\.]+@([\w\-]+\.)+[\w\-]{2,4}$")

MESSAGE_MAX_LENGTH = 5000
NAME_MAX_LENGTH = 100


def email_validator(email: str) -> str:
    if len(email) > EMAIL_MAX_LENGTH or not EMAIL_REGEX.match(email):
        raise ValueError(f"{email} is not a valid email.")
    return email


class ContactUsRequest(BaseModel):
    category: str
    email: Annotated[str, AfterValidator(email_validator)]
    name: str = Field(max_length=NAME_MAX_LENGTH)
    message: str = Field(max_length=MESSAGE_MAX_LENGTH)
    token: str
    data: dict[str, Any] | None = None
    user_id: str | None = None
