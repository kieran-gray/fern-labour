import logging
from uuid import UUID

from app.application.dtos.labour import LabourDTO
from app.application.dtos.labour_summary import LabourSummaryDTO
from app.domain.labour.entity import Labour
from app.domain.labour.exceptions import InvalidLabourId, LabourNotFoundById
from app.domain.labour.repository import LabourRepository
from app.domain.labour.vo_labour_id import LabourId
from app.domain.user.exceptions import UserDoesNotHaveActiveLabour
from app.domain.user.vo_user_id import UserId

log = logging.getLogger(__name__)


class GetLabourService:
    def __init__(self, labour_repository: LabourRepository):
        self._labour_repository = labour_repository

    async def _get_active_labour(self, birthing_person_id: str) -> Labour:
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(
            birthing_person_id=domain_id
        )
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

        return labour

    async def get_labour_by_id(self, labour_id: str) -> LabourDTO:
        try:
            domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

        labour = await self._labour_repository.get_by_id(labour_id=domain_id)
        if not labour:
            raise LabourNotFoundById(labour_id=labour_id)
        return LabourDTO.from_domain(labour)

    async def get_active_labour(self, birthing_person_id: str) -> LabourDTO:
        labour = await self._get_active_labour(birthing_person_id=birthing_person_id)
        return LabourDTO.from_domain(labour)

    async def get_active_labour_summary(self, birthing_person_id: str) -> LabourSummaryDTO:
        labour = await self._get_active_labour(birthing_person_id=birthing_person_id)
        return LabourSummaryDTO.from_domain(labour)
