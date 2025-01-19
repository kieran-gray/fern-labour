import logging
from typing import Any

from app.application.events.event_handler import EventHandler
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.exceptions import SubscriberNotFoundById
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId

log = logging.getLogger(__name__)


class BirthingPersonRemovedSubscriberEventHandler(EventHandler):
    def __init__(self, subscriber_repository: SubscriberRepository):
        self._subscriber_repository = subscriber_repository

    async def handle(self, event: dict[str, Any]) -> None:
        birthing_person_id = BirthingPersonId(event["data"]["birthing_person_id"])
        subscriber_id = SubscriberId(event["data"]["subscriber_id"])
        subscriber = await self._subscriber_repository.get_by_id(subscriber_id)
        if not subscriber:
            raise SubscriberNotFoundById(subscriber_id=subscriber_id)

        subscriber.unsubscribe_from(birthing_person_id=birthing_person_id, removed=True)
        await self._subscriber_repository.save(subscriber)
        log.info(
            f"Removed birthing person '{birthing_person_id.value}' from subscriber '{subscriber_id.value}' "
        )
