from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: str
