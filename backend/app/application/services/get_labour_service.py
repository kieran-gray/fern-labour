import logging

from app.application.dtos.labour import LabourDTO
from app.application.dtos.labour_summary import LabourSummaryDTO
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour
from app.domain.labour.repository import LabourRepository

log = logging.getLogger(__name__)


class GetLabourService:
    def __init__(self, labour_repository: LabourRepository):
        self._labour_repository = labour_repository

    async def _get_active_labour(self, birthing_person_id: str) -> Labour:
        domain_id = BirthingPersonId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(
            birthing_person_id=domain_id
        )
        if not labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        return labour

    async def get_active_labour(self, birthing_person_id: str) -> LabourDTO:
        labour = await self._get_active_labour(birthing_person_id=birthing_person_id)
        return LabourDTO.from_domain(labour)

    async def get_active_labour_summary(self, birthing_person_id: str) -> LabourSummaryDTO:
        labour = await self._get_active_labour(birthing_person_id=birthing_person_id)
        return LabourSummaryDTO.from_domain(labour)
