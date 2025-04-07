import logging
from typing import Any
from uuid import UUID

from app.labour.domain.labour.exceptions import InvalidLabourId, InvalidLabourUpdateId
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId
from app.notification.application.dtos.notification import NotificationDTO
from app.notification.application.gateways.email_notification_gateway import (
    EmailNotificationGateway,
)
from app.notification.application.gateways.notfication_gateway import NotificationGateway
from app.notification.application.gateways.sms_notification_gateway import SMSNotificationGateway
from app.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from app.notification.domain.entity import Notification
from app.notification.domain.enums import NotificationStatus
from app.notification.domain.exceptions import (
    InvalidNotificationId,
    InvalidNotificationStatus,
    NotificationNotFoundByExternalId,
    NotificationNotFoundById,
)
from app.notification.domain.repository import NotificationRepository
from app.notification.domain.value_objects.notification_id import NotificationId
from app.subscription.domain.enums import ContactMethod
from app.subscription.domain.exceptions import InvalidContactMethod
from app.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        email_notification_gateway: EmailNotificationGateway,
        sms_notification_gateway: SMSNotificationGateway,
        notification_generation_service: NotificationGenerationService,
        notification_repository: NotificationRepository,
    ):
        self._email_notification_gateway = email_notification_gateway
        self._sms_notification_gateway = sms_notification_gateway
        self._notification_generation_service = notification_generation_service
        self._notification_repository = notification_repository

    def _get_notification_gateway(self, notification_type: ContactMethod) -> NotificationGateway:
        if notification_type is ContactMethod.EMAIL:
            return self._email_notification_gateway
        elif notification_type is ContactMethod.SMS:
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
        labour_id: str | None = None,
        from_user_id: str | None = None,
        to_user_id: str | None = None,
        labour_update_id: str | None = None,
    ) -> NotificationDTO:
        try:
            domain_labour_id = LabourId(UUID(labour_id)) if labour_id else None
        except ValueError:
            raise InvalidLabourId()

        try:
            domain_labour_update_id = (
                LabourUpdateId(UUID(labour_update_id)) if labour_update_id else None
            )
        except ValueError:
            raise InvalidLabourUpdateId()

        try:
            contact_method = ContactMethod(type)
        except ValueError:
            raise InvalidContactMethod(contact_method=type)

        try:
            notification_status = NotificationStatus(status) if status else None
        except ValueError:
            raise InvalidNotificationStatus(notification_status=status)

        notification = Notification.create(
            labour_id=domain_labour_id,
            from_user_id=UserId(from_user_id) if from_user_id else None,
            to_user_id=UserId(to_user_id) if to_user_id else None,
            type=contact_method,
            destination=destination,
            template=template,
            data=data,
            status=notification_status,
            labour_update_id=domain_labour_update_id,
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

        notification.status = notification_status
        if external_id:
            notification.external_id = external_id
        await self._notification_repository.save(notification=notification)

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

        notification.status = result.status
        await self._notification_repository.save(notification=notification)
