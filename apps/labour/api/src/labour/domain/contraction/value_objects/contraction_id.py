from dataclasses import dataclass
from uuid import UUID

from fern_labour_core.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class ContractionId(ValueObject):
    value: UUID
