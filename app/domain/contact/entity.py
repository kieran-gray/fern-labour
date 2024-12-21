from dataclasses import dataclass, field
from typing import Self
from uuid import uuid4

from app.domain.base.entity import Entity
from app.domain.contact.enums import ContactMethod
from app.domain.contact.vo_contact_id import ContactId


@dataclass(eq=False, kw_only=True)
class Contact(Entity[ContactId]):
    name: str
    phone_number: str | None = None
    email: str | None = None
    contact_methods: list[ContactMethod] = field(default_factory=list)

    @classmethod
    def create(
        cls, *, name: str, phone_number: str, email: str, contact_methods: list[str]
    ) -> Self:
        return cls(
            id_=ContactId(uuid4()),
            name=name,
            phone_number=phone_number,
            email=email,
            contact_methods=[ContactMethod(method) for method in contact_methods],
        )
