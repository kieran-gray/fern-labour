import re
from dataclasses import dataclass

from app.domain.base.value_object import ValueObject
from app.domain.constants.user import PATTERN_EMAIL, USERNAME_MAX_LEN, USERNAME_MIN_LEN
from app.domain.exceptions.user import UsernameInvalid, UsernameTooLong, UsernameTooShort


@dataclass(frozen=True, repr=False)
class Username(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()

        if not re.fullmatch(PATTERN_EMAIL, self.value):
            raise UsernameInvalid(self.value)

        if not len(self.value) >= USERNAME_MIN_LEN:
            raise UsernameTooLong(self.value)

        if not len(self.value) <= USERNAME_MAX_LEN:
            raise UsernameTooShort(self.value)
