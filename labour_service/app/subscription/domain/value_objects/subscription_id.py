from dataclasses import dataclass
from uuid import UUID

from app.common.domain.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class SubscriptionId(ValueObject):
    value: UUID
