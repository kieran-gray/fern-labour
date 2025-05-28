import logging
from typing import Any
from uuid import UUID

from fern_labour_core.events.producer import EventProducer
from fern_labour_notifications_shared.enums import NotificationTemplate

from src.notification.application.dtos.notification import NotificationDTO
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.application.services.notification_router import NotificationRouter
from src.notification.domain.entity import Notification
from src.notification.domain.enums import (
    NotificationChannel,
    NotificationStatus,
)
from src.notification.domain.exceptions import (
    InvalidNotificationChannel,
    InvalidNotificationId,
    InvalidNotificationStatus,
    InvalidNotificationTemplate,
    NotificationNotFoundById,
)
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.services.can_resend_notification_service import (
    CanResendNotificationService,
)
from src.notification.domain.value_objects.notification_id import NotificationId

log = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        notification_router: NotificationRouter,
        notification_generation_service: NotificationGenerationService,
        notification_repository: NotificationRepository,
        event_producer: EventProducer,
    ):
        self._notification_router = notification_router
        self._notification_generation_service = notification_generation_service
        self._notification_repository = notification_repository
        self._event_producer = event_producer

    async def _get_notification(self, notification_id: str) -> Notification:
        try:
            domain_notification_id = NotificationId(UUID(notification_id))
        except ValueError:
            raise InvalidNotificationId(notification_id=notification_id)

        notification = await self._notification_repository.get_by_id(
            notification_id=domain_notification_id
        )
        if not notification:
            raise NotificationNotFoundById(notification_id=notification_id)

        return notification

    async def _send_notification(self, notification: Notification) -> None:
        notification_content = await self._notification_generation_service.generate_content(
            notification=notification
        )

        notification_dto = NotificationDTO.from_domain(notification=notification)
        notification_dto.add_notification_content(content=notification_content)

        result = await self._notification_router.route_notification(notification_dto)

        if result.external_id:
            notification.external_id = result.external_id

        notification.update_status(result.status)

        await self._notification_repository.save(notification=notification)

        await self._event_producer.publish_batch(notification.clear_domain_events())

    async def create_notification(
        self,
        channel: str,
        destination: str,
        template: str,
        data: dict[str, Any],
        status: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> NotificationDTO:
        try:
            notification_channel = NotificationChannel(channel)
        except ValueError:
            raise InvalidNotificationChannel(notification_channel=channel)

        try:
            notification_status = NotificationStatus(status) if status else None
        except ValueError:
            raise InvalidNotificationStatus(notification_status=status)

        try:
            notification_template = NotificationTemplate(template)
        except ValueError:
            raise InvalidNotificationTemplate(template=template)

        notification = Notification.create(
            channel=notification_channel,
            destination=destination,
            template=notification_template,
            data=data,
            metadata=metadata,
            status=notification_status,
        )
        await self._notification_repository.save(notification)

        return NotificationDTO.from_domain(notification)

    async def send(self, notification_id: str) -> None:
        notification = await self._get_notification(notification_id=notification_id)
        await self._send_notification(notification=notification)

    async def resend(self, notification_id: str) -> None:
        notification = await self._get_notification(notification_id=notification_id)
        CanResendNotificationService().can_resend_notification(notification=notification)
        await self._send_notification(notification=notification)
