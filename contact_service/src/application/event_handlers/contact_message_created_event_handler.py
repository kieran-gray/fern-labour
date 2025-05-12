import logging
from dataclasses import dataclass
from typing import Any

from fern_labour_core.events.event import DomainEvent
from fern_labour_core.events.event_handler import EventHandler
from fern_labour_core.events.producer import EventProducer
from fern_labour_notifications_shared.enums import NotificationChannel, NotificationTemplate
from fern_labour_notifications_shared.events import NotificationRequested

from src.application.contact_message_query_service import ContactMessageQueryService

log = logging.getLogger(__name__)


@dataclass
class ContactMessageCreatedMetadata:
    from_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {"from_user_id": self.from_user_id}


class ContactMessageCreatedEventHandler(EventHandler):
    def __init__(
        self,
        contact_message_query_service: ContactMessageQueryService,
        event_producer: EventProducer,
        contact_email: str,
    ):
        self._contact_message_query_service = contact_message_query_service
        self._event_producer = event_producer
        self._contact_email = contact_email
        self._template = NotificationTemplate.CONTACT_US_SUBMISSION

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = DomainEvent.from_dict(event=event)
        contact_message_id = domain_event.data["contact_message_id"]

        contact_message = await self._contact_message_query_service.get_message(
            contact_message_id=contact_message_id
        )
        notification_metadata = ContactMessageCreatedMetadata(
            from_user_id=contact_message.user_id or "null"
        )
        notification_event = NotificationRequested.create(
            data={
                "channel": NotificationChannel.EMAIL,
                "destination": self._contact_email,
                "template": self._template.value,
                "data": contact_message.to_dict(),
                "metadata": notification_metadata.to_dict(),
            }
        )
        await self._event_producer.publish(event=notification_event)
