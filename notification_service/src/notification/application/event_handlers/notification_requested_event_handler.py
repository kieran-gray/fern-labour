import logging
from typing import Any

from fern_labour_core.events.event_handler import EventHandler

from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.events import NotificationRequested, NotificationRequestedData

log = logging.getLogger(__name__)


class NotificationRequestedEventHandler(EventHandler):
    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = NotificationRequested.from_dict(event=event)
        event_data = NotificationRequestedData.from_dict(domain_event.data)

        await self._notification_service.create_notification(
            channel=event_data.channel,
            destination=event_data.destination,
            template=event_data.template,
            data=event_data.data,
            metadata=event_data.metadata,
        )
