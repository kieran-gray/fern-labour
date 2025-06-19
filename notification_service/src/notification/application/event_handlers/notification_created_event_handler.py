import logging
from typing import Any

from fern_labour_core.events.event_handler import EventHandler

from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.events import NotificationCreated, NotificationCreatedData

log = logging.getLogger(__name__)


class NotificationCreatedEventHandler(EventHandler):
    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = NotificationCreated.from_dict(event=event)
        event_data = NotificationCreatedData.from_dict(domain_event.data)

        await self._notification_service.send(notification_id=event_data.notification_id)
