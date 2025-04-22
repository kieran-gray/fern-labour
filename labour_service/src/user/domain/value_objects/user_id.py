from dataclasses import dataclass

from src.core.domain.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: str
