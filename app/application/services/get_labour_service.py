import logging

from app.application.dtos.labour import LabourDTO
from app.application.dtos.labour_summary import LabourSummaryDTO
from app.domain.birthing_person.exceptions import (
    BirthingPersonDoesNotHaveActiveLabour,
    BirthingPersonNotFoundById,
)
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId

log = logging.getLogger(__name__)


class GetLabourService:
    def __init__(self, birthing_person_repository: BirthingPersonRepository):
        self._birthing_person_repository = birthing_person_repository

    async def get_active_labour(self, birthing_person_id: str) -> LabourDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(domain_id)
        if not birthing_person:
            raise BirthingPersonNotFoundById(birthing_person_id=birthing_person_id)

        active_labour = birthing_person.active_labour
        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        return LabourDTO.from_domain(active_labour)

    async def get_active_labour_summary(self, birthing_person_id: str) -> LabourSummaryDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(domain_id)
        if not birthing_person:
            raise BirthingPersonNotFoundById(birthing_person_id=birthing_person_id)

        active_labour = birthing_person.active_labour
        if not active_labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        return LabourSummaryDTO.from_domain(active_labour)
