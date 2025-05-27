import logging

from fern_labour_core.events.producer import EventProducer

from src.notification.application.services.notification_router import NotificationRouter
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.enums import NotificationStatus
from src.notification.domain.exceptions import (
    InvalidNotificationStatus,
    NotificationNotFoundByExternalId,
)
from src.notification.domain.repository import NotificationRepository

log = logging.getLogger(__name__)


class NotificationDeliveryService:
    def __init__(
        self,
        notification_service: NotificationService,
        notification_router: NotificationRouter,
        notification_repository: NotificationRepository,
        event_producer: EventProducer,
    ):
        self._notification_service = notification_service
        self._notification_router = notification_router
        self._notification_repository = notification_repository
        self._event_producer = event_producer

    async def update_undelivered_notification_delivery_status(self) -> None:
        undelivered = await self._notification_repository.get_undelivered_notifications()
        log.info(f"Found {len(undelivered)} undelivered notifications")
        for notification in undelivered:
            assert notification.external_id

            gateway = self._notification_router.get_gateway(notification.channel)

            status = await gateway.get_status(notification.external_id)
            notification_status = NotificationStatus(status)

            if notification_status is notification.status:
                continue

            notification.update_status(notification_status)

            await self._notification_repository.save(notification=notification)
            log.info(f"Status updated for notification ID {notification.id_}")

            await self._event_producer.publish_batch(notification.clear_domain_events())

    async def delivery_status_callback(self, external_id: str, status: str) -> None:
        try:
            notification_status = NotificationStatus(status)
        except ValueError:
            raise InvalidNotificationStatus(notification_status=status)

        notification = await self._notification_repository.get_by_external_id(
            external_id=external_id
        )
        if not notification:
            raise NotificationNotFoundByExternalId(external_id=external_id)

        notification.update_status(notification_status)

        await self._notification_repository.save(notification=notification)

        await self._event_producer.publish_batch(notification.clear_domain_events())
