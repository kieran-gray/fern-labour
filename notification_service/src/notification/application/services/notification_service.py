import logging
from typing import Any
from uuid import UUID

from src.core.domain.producer import EventProducer
from src.notification.application.dtos.notification import NotificationDTO
from src.notification.application.gateways.email_notification_gateway import (
    EmailNotificationGateway,
)
from src.notification.application.gateways.notfication_gateway import NotificationGateway
from src.notification.application.gateways.sms_notification_gateway import SMSNotificationGateway
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.domain.entity import Notification
from src.notification.domain.enums import NotificationStatus, NotificationTemplate, NotificationType
from src.notification.domain.exceptions import (
    InvalidNotificationId,
    InvalidNotificationStatus,
    InvalidNotificationTemplate,
    InvalidNotificationType,
    NotificationNotFoundByExternalId,
    NotificationNotFoundById,
)
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.value_objects.notification_id import NotificationId

log = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        email_notification_gateway: EmailNotificationGateway,
        sms_notification_gateway: SMSNotificationGateway,
        notification_generation_service: NotificationGenerationService,
        notification_repository: NotificationRepository,
        event_producer: EventProducer,
    ):
        self._email_notification_gateway = email_notification_gateway
        self._sms_notification_gateway = sms_notification_gateway
        self._notification_generation_service = notification_generation_service
        self._notification_repository = notification_repository
        self._event_producer = event_producer

    def _get_notification_gateway(self, notification_type: NotificationType) -> NotificationGateway:
        if notification_type is NotificationType.EMAIL:
            return self._email_notification_gateway
        elif notification_type is NotificationType.SMS:
            return self._sms_notification_gateway
        else:
            raise NotImplementedError(
                f"Notification gateway for type {notification_type.value} not implemented"
            )

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

    async def create_notification(
        self,
        type: str,
        destination: str,
        template: str,
        data: dict[str, Any],
        status: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> NotificationDTO:
        try:
            notification_type = NotificationType(type)
        except ValueError:
            raise InvalidNotificationType(notification_type=type)

        try:
            notification_status = NotificationStatus(status) if status else None
        except ValueError:
            raise InvalidNotificationStatus(notification_status=status)

        try:
            notification_template = NotificationTemplate(template)
        except ValueError:
            raise InvalidNotificationTemplate(template=template)

        notification = Notification.create(
            type=notification_type,
            destination=destination,
            template=notification_template,
            data=data,
            metadata=metadata,
            status=notification_status,
        )
        await self._notification_repository.save(notification)

        return NotificationDTO.from_domain(notification)

    async def update_notification(
        self, notification_id: str, status: str, external_id: str | None = None
    ) -> NotificationDTO:
        try:
            notification_status = NotificationStatus(status)
        except ValueError:
            raise InvalidNotificationStatus(notification_status=status)

        notification = await self._get_notification(notification_id=notification_id)

        if external_id:
            notification.external_id = external_id

        notification.update_status(notification_status)

        await self._notification_repository.save(notification=notification)

        await self._event_producer.publish_batch(notification.clear_domain_events())

        return NotificationDTO.from_domain(notification=notification)

    async def status_callback(self, external_id: str, status: str) -> None:
        try:
            notification_status = NotificationStatus(status)
        except ValueError:
            raise InvalidNotificationStatus(notification_status=status)

        notification = await self._notification_repository.get_by_external_id(
            external_id=external_id
        )
        if not notification:
            raise NotificationNotFoundByExternalId(external_id=external_id)

        notification.status = notification_status
        await self._notification_repository.save(notification=notification)

    async def send(self, notification_id: str) -> None:
        notification = await self._get_notification(notification_id=notification_id)
        notification_content = await self._notification_generation_service.generate_content(
            notification_id=notification_id
        )

        notification_dto = NotificationDTO.from_domain(notification=notification)
        notification_dto.add_notification_content(content=notification_content)

        notification_gateway = self._get_notification_gateway(notification.type)
        result = await notification_gateway.send(notification_dto)

        if result.external_id:
            notification.external_id = result.external_id

        notification.update_status(result.status)

        await self._notification_repository.save(notification=notification)

        await self._event_producer.publish_batch(notification.clear_domain_events())
