from dataclasses import dataclass
from uuid import UUID

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class LabourId(ValueObject):
    value: UUID
