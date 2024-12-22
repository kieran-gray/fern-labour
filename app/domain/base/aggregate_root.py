from dataclasses import dataclass, field
from typing import Generic, TypeVar

from app.domain.base.entity import Entity
from app.domain.base.event import DomainEvent
from app.domain.base.value_object import ValueObject

T = TypeVar("T", bound=ValueObject)


@dataclass
class AggregateRoot(Entity[T], Generic[T]):
    """
    Base class for aggregate root entities
    """

    _domain_events: list[DomainEvent] = field(default_factory=list, init=False, repr=False, compare=False)

    def __init__(self) -> None:
        super().__init__(self)
        self._domain_events: list[DomainEvent] = []

    def add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> list[DomainEvent]:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

    @property
    def domain_events(self) -> list[DomainEvent]:
        return self._domain_events.copy()
