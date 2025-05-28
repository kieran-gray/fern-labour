import logging
from typing import Any

from fern_labour_core.events.event_handler import EventHandler

from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.notification.domain.enums import NotificationChannel, NotificationStatus
from src.notification.domain.events import NotificationStatusUpdated, NotificationStatusUpdatedData

log = logging.getLogger(__name__)


class NotificationStatusUpdatedEventHandler(EventHandler):
    def __init__(self, notification_delivery_service: NotificationDeliveryService):
        self._notification_delivery_service = notification_delivery_service
        self._channels = [NotificationChannel.SMS.value, NotificationChannel.WHATSAPP.value]

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = NotificationStatusUpdated.from_dict(event=event)
        event_data = NotificationStatusUpdatedData.from_dict(domain_event.data)

        if not event_data.external_id:
            return

        if event_data.channel not in self._channels:
            return

        if NotificationStatus(event_data.to_status) is not NotificationStatus.SUCCESS:
            return

        log.info(f"Redacting notification body for notification ID: {event_data.notification_id}")
        await self._notification_delivery_service.redact_delivered_notification_body(
            external_id=event_data.external_id, channel=event_data.channel
        )
