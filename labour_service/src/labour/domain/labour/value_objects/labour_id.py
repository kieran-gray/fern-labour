from dataclasses import dataclass
from uuid import UUID

from src.core.domain.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class LabourId(ValueObject):
    value: UUID
