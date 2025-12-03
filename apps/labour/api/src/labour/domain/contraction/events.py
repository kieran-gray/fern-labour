from dataclasses import dataclass
from typing import Self

from fern_labour_core.events.event import DomainEvent

from src.labour.domain.contraction.entity import Contraction


@dataclass
class ContractionStarted(DomainEvent):
    event_type = "contraction.started"

    @classmethod
    def from_contraction(cls, contraction: Contraction) -> Self:
        labour_id = str(contraction.labour_id.value)
        data = {
            "labour_id": labour_id,
            "start_time": contraction.start_time.isoformat(),
            "notes": contraction.notes if contraction.notes else "",
        }
        return super().create(
            aggregate_id=labour_id,
            aggregate_type="labour",
            data=data,
            event_type=cls.event_type,
        )


@dataclass
class ContractionEnded(DomainEvent):
    event_type: str = "contraction.ended"

    @classmethod
    def from_contraction(cls, contraction: Contraction) -> Self:
        labour_id = str(contraction.labour_id.value)
        data = {
            "labour_id": labour_id,
            "end_time": contraction.end_time.isoformat(),
            "notes": contraction.notes if contraction.notes else "",
        }
        return super().create(
            aggregate_id=labour_id,
            aggregate_type="labour",
            data=data,
            event_type=cls.event_type,
        )
