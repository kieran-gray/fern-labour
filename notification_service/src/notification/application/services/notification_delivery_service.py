import logging

from fern_labour_core.unit_of_work import UnitOfWork

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.domain.domain_event.repository import DomainEventRepository
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
        domain_event_repository: DomainEventRepository,
        domain_event_publisher: DomainEventPublisher,
        unit_of_work: UnitOfWork,
    ):
        self._notification_service = notification_service
        self._notification_router = notification_router
        self._notification_repository = notification_repository
        self._domain_event_repository = domain_event_repository
        self._domain_event_publisher = domain_event_publisher
        self._unit_of_work = unit_of_work

    async def update_undelivered_notification_delivery_status(self) -> None:
        undelivered = await self._notification_repository.get_undelivered_notifications()
        log.info(f"Found {len(undelivered)} undelivered notifications")
        for notification in undelivered:
            assert notification.external_id

            gateway = self._notification_router.get_gateway(notification.channel)

            status = await gateway.get_status(notification.external_id)
            if not status:
                continue

            notification_status = NotificationStatus(status)
            if notification_status is notification.status:
                continue

            notification.update_status(notification_status)

            async with self._unit_of_work:
                await self._notification_repository.save(notification=notification)
                await self._domain_event_repository.save_many(notification.clear_domain_events())

            log.info(f"Status updated for notification ID {notification.id_}")

        await self._domain_event_publisher.publish_batch()

    async def redact_delivered_notification_body(self, external_id: str, channel: str) -> None:
        gateway = self._notification_router.get_gateway(channel=channel)
        await gateway.redact_notification_body(external_id=external_id)

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

        async with self._unit_of_work:
            await self._notification_repository.save(notification=notification)
            await self._domain_event_repository.save_many(notification.clear_domain_events())

        self._domain_event_publisher.publish_batch_in_background()
