from dataclasses import dataclass
from uuid import UUID

from app.domain.base.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: UUID
