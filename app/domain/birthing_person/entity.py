from dataclasses import dataclass, field
from typing import Self

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour
from app.domain.subscriber.vo_subscriber_id import SubscriberId


@dataclass(eq=False, kw_only=True)
class BirthingPerson(AggregateRoot[BirthingPersonId]):
    first_name: str
    last_name: str
    labours: list[Labour] = field(default_factory=list)
    subscribers: list[SubscriberId] = field(default_factory=list)

    @classmethod
    def create(cls, *, birthing_person_id: str, first_name: str, last_name: str) -> Self:
        return cls(
            id_=BirthingPersonId(birthing_person_id),
            first_name=first_name,
            last_name=last_name,
        )

    @property
    def has_active_labour(self) -> bool:
        return any(labour.is_active for labour in self.labours)

    @property
    def active_labour(self) -> Labour | None:
        return next((labour for labour in self.labours if labour.is_active), None)

    def add_subscriber(self, subscriber: SubscriberId) -> None:
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: SubscriberId) -> None:
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def add_labour(self, labour: Labour) -> None:
        if labour not in self.labours:
            self.labours.append(labour)
