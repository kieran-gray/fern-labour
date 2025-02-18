from dataclasses import dataclass, field
from typing import Self

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour


@dataclass(eq=False, kw_only=True)
class BirthingPerson(AggregateRoot[BirthingPersonId]):
    first_name: str
    last_name: str
    phone_number: str | None = None
    email: str | None = None
    labours: list[Labour] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        birthing_person_id: str,
        first_name: str,
        last_name: str,
        phone_number: str | None = None,
        email: str | None = None,
    ) -> Self:
        return cls(
            id_=BirthingPersonId(birthing_person_id),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
        )

    @property
    def active_labour(self) -> Labour | None:
        return next((labour for labour in self.labours if labour.is_active), None)
