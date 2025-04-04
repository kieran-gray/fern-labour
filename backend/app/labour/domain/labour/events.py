from dataclasses import dataclass
from typing import Any, Self

from app.common.domain.event import DomainEvent


@dataclass
class LabourPlanned(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "labour.planned") -> Self:
        return super().create(event_type=event_type, data=data)


@dataclass
class LabourBegun(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "labour.begun") -> Self:
        return super().create(event_type=event_type, data=data)


@dataclass
class LabourCompleted(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "labour.completed") -> Self:
        return super().create(event_type=event_type, data=data)


@dataclass
class LabourUpdatePosted(DomainEvent):
    @classmethod
    def create(cls, data: dict[str, Any], event_type: str = "labour.update-posted") -> Self:
        return super().create(event_type=event_type, data=data)
