import logging
from typing import Any

from app.application.events.event_handler import EventHandler
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.vo_subscriber_id import SubscriberId

log = logging.getLogger(__name__)


class SubscriberSubscribedToEventHandler(EventHandler):
    def __init__(self, birthing_person_repository: BirthingPersonRepository):
        self._birthing_person_repository = birthing_person_repository

    async def handle(self, event: dict[str, Any]) -> None:
        birthing_person_id = BirthingPersonId(event["data"]["birthing_person_id"])
        subscriber_id = SubscriberId(event["data"]["subscriber_id"])
        birthing_person = await self._birthing_person_repository.get_by_id(birthing_person_id)
        if not birthing_person:
            # TODO should probably raise an error instead?
            log.error(f"Could not find birthing person by id '{birthing_person_id.value}'")
            return

        birthing_person.add_subscriber(subscriber_id)
        await self._birthing_person_repository.save(birthing_person)
        log.info(
            f"Added subscriber '{subscriber_id.value}' to birthing person '{birthing_person_id.value}'"
        )
