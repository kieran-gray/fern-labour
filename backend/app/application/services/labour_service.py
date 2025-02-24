import logging
from datetime import datetime

from app.application.dtos.labour import LabourDTO
from app.application.events.producer import EventProducer
from app.application.services.user_service import UserService
from app.domain.labour.entity import Labour
from app.domain.labour.repository import LabourRepository
from app.domain.labour_update.enums import LabourUpdateType
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.complete_labour import CompleteLabourService
from app.domain.services.end_contraction import EndContractionService
from app.domain.services.post_labour_update import PostLabourUpdateService
from app.domain.services.start_contraction import StartContractionService
from app.domain.user.exceptions import UserDoesNotHaveActiveLabour, UserHasActiveLabour
from app.domain.user.vo_user_id import UserId

log = logging.getLogger(__name__)


class LabourService:
    def __init__(
        self,
        user_service: UserService,
        labour_repository: LabourRepository,
        event_producer: EventProducer,
    ):
        self._user_service = user_service
        self._labour_repository = labour_repository
        self._event_producer = event_producer

    async def plan_labour(
        self,
        birthing_person_id: str,
        first_labour: bool,
        due_date: datetime,
        labour_name: str | None = None,
    ) -> LabourDTO:
        domain_id = UserId(birthing_person_id)
        _ = await self._user_service.get(birthing_person_id)
        existing_labour = await self._labour_repository.get_active_labour_by_birthing_person_id(
            domain_id
        )
        if existing_labour:
            raise UserHasActiveLabour(user_id=birthing_person_id)

        labour = Labour.plan(
            birthing_person_id=domain_id,
            first_labour=first_labour,
            due_date=due_date,
            labour_name=labour_name,
        )

        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def update_labour_plan(
        self,
        birthing_person_id: str,
        first_labour: bool,
        due_date: datetime,
        labour_name: str | None = None,
    ) -> LabourDTO:
        domain_id = UserId(birthing_person_id)
        _ = await self._user_service.get(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

        labour.update_plan(first_labour=first_labour, due_date=due_date, labour_name=labour_name)

        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def begin_labour(self, birthing_person_id: str) -> LabourDTO:
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

        labour = BeginLabourService().begin_labour(labour=labour)
        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def complete_labour(
        self, birthing_person_id: str, end_time: datetime | None = None, notes: str | None = None
    ) -> LabourDTO:
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

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
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

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
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

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
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

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
