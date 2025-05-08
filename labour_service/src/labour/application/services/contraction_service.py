import logging
from datetime import datetime
from uuid import UUID

from src.labour.application.dtos.labour import LabourDTO
from src.labour.domain.contraction.exceptions import ContractionIdInvalid
from src.labour.domain.contraction.services.delete_contraction import DeleteContractionService
from src.labour.domain.contraction.services.end_contraction import EndContractionService
from src.labour.domain.contraction.services.start_contraction import StartContractionService
from src.labour.domain.contraction.services.update_contraction import UpdateContractionService
from src.labour.domain.contraction.value_objects.contraction_id import ContractionId
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.repository import LabourRepository
from src.user.domain.exceptions import UserDoesNotHaveActiveLabour
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class ContractionService:
    def __init__(self, labour_repository: LabourRepository):
        self._labour_repository = labour_repository

    async def _get_labour(self, birthing_person_id: str) -> Labour:
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)
        return labour

    async def start_contraction(
        self,
        birthing_person_id: str,
        intensity: int | None = None,
        start_time: datetime | None = None,
        notes: str | None = None,
    ) -> LabourDTO:
        labour = await self._get_labour(birthing_person_id=birthing_person_id)

        labour = StartContractionService().start_contraction(
            labour=labour, intensity=intensity, start_time=start_time, notes=notes
        )
        await self._labour_repository.save(labour)

        return LabourDTO.from_domain(labour)

    async def end_contraction(
        self,
        birthing_person_id: str,
        intensity: int,
        end_time: datetime | None = None,
        notes: str | None = None,
    ) -> LabourDTO:
        labour = await self._get_labour(birthing_person_id=birthing_person_id)

        labour = EndContractionService().end_contraction(
            labour=labour, intensity=intensity, end_time=end_time, notes=notes
        )
        await self._labour_repository.save(labour)

        return LabourDTO.from_domain(labour)

    async def update_contraction(
        self,
        birthing_person_id: str,
        contraction_id: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        intensity: int | None = None,
        notes: str | None = None,
    ) -> LabourDTO:
        labour = await self._get_labour(birthing_person_id=birthing_person_id)

        try:
            contraction_domain_id = ContractionId(UUID(contraction_id))
        except ValueError:
            raise ContractionIdInvalid(contraction_id=contraction_id)

        labour = UpdateContractionService().update_contraction(
            labour=labour,
            contraction_id=contraction_domain_id,
            start_time=start_time,
            end_time=end_time,
            intensity=intensity,
            notes=notes,
        )
        await self._labour_repository.save(labour)

        return LabourDTO.from_domain(labour)

    async def delete_contraction(self, birthing_person_id: str, contraction_id: str) -> LabourDTO:
        labour = await self._get_labour(birthing_person_id=birthing_person_id)

        try:
            contraction_domain_id = ContractionId(UUID(contraction_id))
        except ValueError:
            raise ContractionIdInvalid(contraction_id=contraction_id)

        labour = DeleteContractionService().delete_contraction(
            labour=labour,
            contraction_id=contraction_domain_id,
        )
        await self._labour_repository.save(labour)

        return LabourDTO.from_domain(labour)
