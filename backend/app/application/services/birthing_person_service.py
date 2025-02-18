import logging

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.application.dtos.birthing_person_summary import BirthingPersonSummaryDTO
from app.application.events.producer import EventProducer
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import (
    BirthingPersonExistsWithID,
    BirthingPersonNotFoundById,
)
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId

log = logging.getLogger(__name__)


class BirthingPersonService:
    def __init__(
        self, birthing_person_repository: BirthingPersonRepository, event_producer: EventProducer
    ):
        self._birthing_person_repository = birthing_person_repository
        self._event_producer = event_producer

    async def register(
        self,
        birthing_person_id: str,
        first_name: str,
        last_name: str,
        phone_number: str | None = None,
        email: str | None = None,
    ) -> BirthingPersonDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(domain_id)
        if birthing_person:
            raise BirthingPersonExistsWithID(birthing_person_id=birthing_person_id)

        birthing_person = BirthingPerson.create(
            birthing_person_id=birthing_person_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
        )
        await self._birthing_person_repository.save(birthing_person)
        return BirthingPersonDTO.from_domain(birthing_person)

    async def get_birthing_person(self, birthing_person_id: str) -> BirthingPersonDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(domain_id)
        if not birthing_person:
            raise BirthingPersonNotFoundById(birthing_person_id=birthing_person_id)

        return BirthingPersonDTO.from_domain(birthing_person)

    async def get_birthing_person_summary(
        self, birthing_person_id: str
    ) -> BirthingPersonSummaryDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(domain_id)
        if not birthing_person:
            raise BirthingPersonNotFoundById(birthing_person_id=birthing_person_id)

        return BirthingPersonSummaryDTO.from_domain(birthing_person)
