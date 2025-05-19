from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from fern_labour_core.events.event import DomainEvent

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour_update.entity import LabourUpdate


@dataclass
class LabourPlanned(DomainEvent):
    event_type: str = "labour.planned"

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        data = {
            "labour_id": str(labour.id_.value),
            "birthing_person_id": labour.birthing_person_id.value,
        }
        return super().create(event_type=cls.event_type, data=data)


@dataclass
class LabourBegun(DomainEvent):
    event_type: str = "labour.begun"

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        start_time = labour.start_time or datetime.now(UTC)
        data = {
            "labour_id": str(labour.id_.value),
            "birthing_person_id": labour.birthing_person_id.value,
            "start_time": start_time,
        }
        return super().create(event_type=cls.event_type, data=data)


@dataclass
class LabourCompleted(DomainEvent):
    event_type: str = "labour.completed"

    @classmethod
    def from_domain(cls, labour: Labour) -> Self:
        end_time = labour.end_time or datetime.now(UTC)
        data = {
            "labour_id": str(labour.id_.value),
            "birthing_person_id": labour.birthing_person_id.value,
            "end_time": end_time,
            "notes": labour.notes if labour.notes else "",
        }
        return super().create(event_type=cls.event_type, data=data)


@dataclass
class LabourUpdatePosted(DomainEvent):
    event_type: str = "labour.update-posted"

    @classmethod
    def from_domain(cls, labour: Labour, labour_update: LabourUpdate) -> Self:
        data = {
            "birthing_person_id": labour.birthing_person_id.value,
            "labour_id": str(labour.id_.value),
            "labour_update_type": labour_update.labour_update_type.value,
            "labour_update_id": str(labour_update.id_.value),
            "message": labour_update.message,
            "sent_time": labour_update.sent_time.isoformat(),
        }
        return super().create(event_type=cls.event_type, data=data)
