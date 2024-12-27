from dataclasses import dataclass

from app.domain.base.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class BirthingPersonId(ValueObject):
    value: str
