from dataclasses import dataclass
from typing import Any, Self

from app.domain.base.event import DomainEvent
from app.domain.contraction.entity import Contraction


@dataclass
class LabourBegun(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any]) -> Self:
        event_type = "labour.begun"
        return super().create(event_type=event_type, data=data)


@dataclass
class LabourCompleted(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any]) -> Self:
        event_type = "labour.completed"
        return super().create(event_type=event_type, data=data)


@dataclass
class ContractionStarted(DomainEvent):
    @classmethod
    def from_contraction(cls, contraction: Contraction) -> Self:
        event_type = "contraction.started"
        data = {
            "labour_id": str(contraction.id_.value),
            "start_time": contraction.start_time.isoformat(),
            "notes": contraction.notes if contraction.notes else "",
        }
        return super().create(event_type=event_type, data=data)


@dataclass
class ContractionEnded(DomainEvent):
    @classmethod
    def from_contraction(cls, contraction: Contraction) -> Self:
        event_type = "contraction.ended"
        data = {
            "labour_id": str(contraction.labour_id.value),
            "end_time": contraction.end_time.isoformat(),
            "notes": contraction.notes if contraction.notes else "",
        }
        return super().create(event_type=event_type, data=data)
