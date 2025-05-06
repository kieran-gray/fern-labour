import logging
from uuid import UUID

from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.dtos.labour_summary import LabourSummaryDTO
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.exceptions import (
    InvalidLabourId,
    LabourAlreadyCompleted,
    LabourNotFoundById,
)
from src.labour.domain.labour.repository import LabourRepository
from src.labour.domain.labour.services.can_accept_subscriber import CanAcceptSubscriberService
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.user.domain.exceptions import UserDoesNotHaveActiveLabour
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class LabourQueryService:
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

    async def get_all_labours(self, birthing_person_id: str) -> list[LabourDTO]:
        domain_id = UserId(birthing_person_id)
        labours = await self._labour_repository.get_labours_by_birthing_person_id(
            birthing_person_id=domain_id
        )
        return [LabourDTO.from_domain(labour) for labour in labours]

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

    async def can_accept_subscriber(self, subscriber_id: str, labour_id: str) -> None:
        try:
            domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

        labour = await self._labour_repository.get_by_id(labour_id=domain_id)
        if not labour:
            raise LabourNotFoundById(labour_id=labour_id)

        return CanAcceptSubscriberService().can_accept_subscriber(
            labour=labour,
            subscriber_id=UserId(subscriber_id),
        )

    async def ensure_labour_is_active(self, labour_id: str) -> None:
        try:
            domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

        labour = await self._labour_repository.get_by_id(labour_id=domain_id)
        if not labour:
            raise LabourNotFoundById(labour_id=labour_id)

        if not labour.is_active:
            raise LabourAlreadyCompleted()
