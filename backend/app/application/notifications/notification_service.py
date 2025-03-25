import logging
from typing import Any
from uuid import UUID

from app.application.dtos.notification import NotificationDTO
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    NotificationGateway,
    SMSNotificationGateway,
)
from app.domain.labour.exceptions import InvalidLabourId, InvalidLabourUpdateId
from app.domain.labour.vo_labour_id import LabourId
from app.domain.labour_update.vo_labour_update_id import LabourUpdateId
from app.domain.notification.entity import Notification
from app.domain.notification.enums import NotificationStatus
from app.domain.notification.exceptions import (
    InvalidNotificationId,
    InvalidNotificationStatus,
    NotificationNotFoundById,
)
from app.domain.notification.repository import NotificationRepository
from app.domain.notification.vo_notification_id import NotificationId
from app.domain.subscription.enums import ContactMethod
from app.domain.subscription.exceptions import InvalidContactMethod
from app.domain.user.vo_user_id import UserId

log = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        email_notification_gateway: EmailNotificationGateway,
        sms_notification_gateway: SMSNotificationGateway,
        notification_repository: NotificationRepository,
    ):
        self._email_notification_gateway = email_notification_gateway
        self._sms_notification_gateway = sms_notification_gateway
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

    async def update_notification_status(
        self, notification_id: str, status: str
    ) -> NotificationDTO:
        try:
            domain_notification_id = NotificationId(UUID(notification_id))
        except ValueError:
            raise InvalidNotificationId(notification_id=notification_id)

        try:
            notification_status = NotificationStatus(status)
        except ValueError:
            raise InvalidNotificationStatus(notification_status=status)

        notification = await self._notification_repository.get_by_id(
            notification_id=domain_notification_id
        )
        if not notification:
            raise NotificationNotFoundById(notification_id=notification_id)

        notification.update_status(status=notification_status)
        await self._notification_repository.save(notification=notification)

        return NotificationDTO.from_domain(notification=notification)

    async def send(self, notification: NotificationDTO) -> None:
        try:
            contact_method = ContactMethod(notification.type)
        except ValueError:
            raise InvalidContactMethod(notification.type)

        notification_gateway = self._get_notification_gateway(contact_method)
        result = await notification_gateway.send(notification)
        await self.update_notification_status(notification_id=notification.id, status=result.status)
