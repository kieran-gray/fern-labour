import re

from app.domain.user.constants import PATTERN_EMAIL


def validate_username(value: str) -> str:
    if not re.fullmatch(PATTERN_EMAIL, value):
        raise ValueError("Username is not a valid email address")
    return value
