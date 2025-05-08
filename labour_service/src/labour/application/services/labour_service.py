import logging
from datetime import datetime
from uuid import UUID

from fern_labour_core.events.producer import EventProducer

from src.labour.application.dtos.labour import LabourDTO
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.exceptions import (
    CannotDeleteActiveLabour,
    InvalidLabourId,
    InvalidLabourUpdateId,
    LabourNotFoundById,
    UnauthorizedLabourRequest,
)
from src.labour.domain.labour.repository import LabourRepository
from src.labour.domain.labour.services.begin_labour import BeginLabourService
from src.labour.domain.labour.services.complete_labour import CompleteLabourService
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.labour.domain.labour_update.enums import LabourUpdateType
from src.labour.domain.labour_update.services.post_labour_update import PostLabourUpdateService
from src.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId
from src.user.domain.exceptions import UserDoesNotHaveActiveLabour, UserHasActiveLabour
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class LabourService:
    def __init__(self, labour_repository: LabourRepository, event_producer: EventProducer):
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

    async def delete_labour_update(
        self,
        birthing_person_id: str,
        labour_update_id: str,
    ) -> LabourDTO:
        domain_id = UserId(birthing_person_id)
        labour = await self._labour_repository.get_active_labour_by_birthing_person_id(domain_id)
        if not labour:
            raise UserDoesNotHaveActiveLabour(user_id=birthing_person_id)

        try:
            labour_update_domain_id = LabourUpdateId(UUID(labour_update_id))
        except ValueError:
            raise InvalidLabourUpdateId()

        labour.delete_labour_update(labour_update_id=labour_update_domain_id)

        await self._labour_repository.save(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return LabourDTO.from_domain(labour)

    async def delete_labour(
        self,
        requester_id: str,
        labour_id: str,
    ) -> None:
        try:
            labour_domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

        labour = await self._labour_repository.get_by_id(labour_id=labour_domain_id)
        if not labour:
            raise LabourNotFoundById(labour_id=labour_id)

        if labour.birthing_person_id.value != requester_id:
            raise UnauthorizedLabourRequest()

        if labour.is_active:
            raise CannotDeleteActiveLabour()

        await self._labour_repository.delete(labour)

        await self._event_producer.publish_batch(labour.clear_domain_events())

        return None
