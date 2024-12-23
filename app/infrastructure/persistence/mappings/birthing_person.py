from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import composite, relationship

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.contact.entity import Contact
from app.domain.contact.vo_contact_id import ContactId
from app.domain.labour.entity import Labour
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.birthing_persons import birthing_persons_table
from app.infrastructure.persistence.tables.contacts import contacts_table

mapper_registry.map_imperatively(
    Contact,
    contacts_table,
    properties={
        "id_": composite(ContactId, contacts_table.c.id),
        "birthing_person_id": composite(BirthingPersonId, contacts_table.c.birthing_person_id),
        "name": contacts_table.c.name,
        "phone_number": contacts_table.c.phone_number,
        "email": contacts_table.c.email,
        "contact_methods": contacts_table.c.contact_methods,
    },
    column_prefix="_",
)

mapper_registry.map_imperatively(
    BirthingPerson,
    birthing_persons_table,
    properties={
        "id_": composite(BirthingPersonId, birthing_persons_table.c.id),
        "name": birthing_persons_table.c.name,
        "first_labour": birthing_persons_table.c.first_labour,
        "labours": relationship(Labour, cascade="all"),
        "contacts": relationship(Contact, cascade="all"),
    },
    column_prefix="_",
)


@event.listens_for(BirthingPerson, "load")
def initialize_domain_events(target: Any, _: Any) -> None:
    if not hasattr(target, "_domain_events"):
        target._domain_events = []
