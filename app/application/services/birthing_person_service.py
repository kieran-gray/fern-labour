import logging

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import (
    BirthingPersonExistsWithID,
    BirthingPersonNotFoundById,
)
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.contact.entity import Contact

log = logging.getLogger(__name__)


class BirthingPersonService:
    def __init__(
        self,
        birthing_person_repository: BirthingPersonRepository,
    ):
        self._birthing_person_repository = birthing_person_repository

    async def register(
        self, birthing_person_id: str, name: str, first_labour: bool
    ) -> BirthingPersonDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(domain_id)
        if birthing_person:
            raise BirthingPersonExistsWithID(birthing_person_id=birthing_person_id)

        birthing_person = BirthingPerson.create(
            birthing_person_id=birthing_person_id, name=name, first_labour=first_labour
        )
        await self._birthing_person_repository.save(birthing_person)
        return BirthingPersonDTO.from_domain(birthing_person)

    async def add_contact(
        self,
        birthing_person_id: str,
        name: str,
        contact_methods: list[str],
        phone_number: str | None = None,
        email: str | None = None,
    ) -> BirthingPersonDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(domain_id)
        if not birthing_person:
            raise BirthingPersonNotFoundById(birthing_person_id=birthing_person_id)

        contact = Contact.create(
            name=name, phone_number=phone_number, email=email, contact_methods=contact_methods
        )
        birthing_person.add_contact(contact=contact)
        await self._birthing_person_repository.save(birthing_person)
        return BirthingPersonDTO.from_domain(birthing_person)
