from dataclasses import dataclass
from typing import Self

from fern_labour_core.events.event import DomainEvent

from src.labour.domain.contraction.entity import Contraction


@dataclass
class ContractionStarted(DomainEvent):
    @classmethod
    def from_contraction(
        cls, contraction: Contraction, event_type: str = "contraction.started"
    ) -> Self:
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
