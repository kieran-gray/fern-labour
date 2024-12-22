from dataclasses import dataclass, field
from typing import Self

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.birthing_person.exceptions import (
    ContactAlreadyExists,
    ContactDoesNotExist,
)
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.contact.entity import Contact
from app.domain.labour.entity import Labour


@dataclass(eq=False, kw_only=True)
class BirthingPerson(AggregateRoot[BirthingPersonId]):
    name: str
    first_labour: bool
    labours: list[Labour] = field(default_factory=list)
    contacts: list[Contact] = field(default_factory=list)

    @classmethod
    def create(cls, *, birthing_person_id: str, name: str, first_labour: bool) -> Self:
        return cls(id_=BirthingPersonId(birthing_person_id), name=name, first_labour=first_labour)

    @property
    def has_active_labour(self) -> bool:
        return any(labour.is_active for labour in self.labours)

    @property
    def active_labour(self) -> Labour | None:
        return next((labour for labour in self.labours if labour.is_active), None)

    def add_contact(self, contact: Contact) -> None:
        if contact in self.contacts:
            raise ContactAlreadyExists()
        self.contacts.append(contact)

    def remove_contact(self, contact: Contact) -> None:
        if contact not in self.contacts:
            raise ContactDoesNotExist()
        self.contacts.remove(contact)

    def add_labour(self, labour: Labour) -> None:
        self.labours.append(labour)
