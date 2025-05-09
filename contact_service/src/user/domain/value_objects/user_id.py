from dataclasses import dataclass

from fern_labour_core.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: str
