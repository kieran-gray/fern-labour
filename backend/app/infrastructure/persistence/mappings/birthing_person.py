from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite, relationship

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.birthing_persons import birthing_persons_table

mapper_registry.map_imperatively(
    BirthingPerson,
    birthing_persons_table,
    properties={
        "id_": composite(BirthingPersonId, birthing_persons_table.c.id),
        "first_name": birthing_persons_table.c.first_name,
        "last_name": birthing_persons_table.c.last_name,
        "phone_number": birthing_persons_table.c.phone_number,
        "email": birthing_persons_table.c.email,
        "labours": relationship(Labour, cascade="all"),
    },
    column_prefix="_",
)


@event.listens_for(BirthingPerson, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
