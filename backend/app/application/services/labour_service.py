import logging
from datetime import datetime

from app.application.dtos.labour import LabourDTO
from app.application.events.producer import EventProducer
from app.application.services.birthing_person_service import BirthingPersonService
from app.domain.birthing_person.exceptions import (
    BirthingPersonDoesNotHaveActiveLabour,
    BirthingPersonHasActiveLabour,
)
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.repository import LabourRepository
from app.domain.labour_update.enums import LabourUpdateType
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.complete_labour import CompleteLabourService
from app.domain.services.end_contraction import EndContractionService
from app.domain.services.plan_labour import PlanLabourService
from app.domain.services.post_labour_update import PostLabourUpdateService
from app.domain.services.start_contraction import StartContractionService

log = logging.getLogger(__name__)


class LabourService:
    def __init__(
        self,
        birthing_person_service: BirthingPersonService,
        labour_repository: LabourRepository,
        event_producer: EventProducer,
    ):
        self._birthing_person_service = birthing_person_service
        self._labour_repository = labour_repository
        self._event_producer = event_producer

    async def plan_labour(
        self,
        birthing_person_id: str,
        first_labour: bool,
        due_date: datetime,
        labour_name: str | None = None,
    ) -> LabourDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        _ = await self._birthing_person_service.get_birthing_person(birthing_person_id)
        existing_labour = await self._labour_repository.get_active_labour_by_birthing_person_id(
            domain_id
        )
        if existing_labour:
            raise BirthingPersonHasActiveLabour(birthing_person_id=birthing_person_id)

        labour = PlanLabourService().plan_labour(
            birthing_person_id=domain_id,
            first_labour=first_labour,
            due_date=due_date,
            labour_name=labour_name,
        )
        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def begin_labour(self, birthing_person_id: str) -> LabourDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        labour = BeginLabourService().begin_labour(labour=labour)
        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def complete_labour(
        self, birthing_person_id: str, end_time: datetime | None = None, notes: str | None = None
    ) -> LabourDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        labour = CompleteLabourService().complete_labour(
            labour=labour, end_time=end_time, notes=notes
        )
        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def start_contraction(
        self,
        birthing_person_id: str,
        intensity: int | None = None,
        start_time: datetime | None = None,
        notes: str | None = None,
    ) -> LabourDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        labour = StartContractionService().start_contraction(
            labour=labour, intensity=intensity, start_time=start_time, notes=notes
        )

        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def end_contraction(
        self,
        birthing_person_id: str,
        intensity: int,
        end_time: datetime | None = None,
        notes: str | None = None,
    ) -> LabourDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        labour = EndContractionService().end_contraction(
            labour=labour, intensity=intensity, end_time=end_time, notes=notes
        )
        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def post_labour_update(
        self,
        birthing_person_id: str,
        labour_update_type: str,
        message: str,
        sent_time: datetime | None = None,
    ) -> LabourDTO:
        domain_id = BirthingPersonId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise BirthingPersonDoesNotHaveActiveLabour(birthing_person_id=birthing_person_id)

        labour_update_type_enum = LabourUpdateType(labour_update_type)
        labour = PostLabourUpdateService().post_labour_update(
            labour=labour,
            labour_update_type=labour_update_type_enum,
            message=message,
            sent_time=sent_time,
        )
        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)
