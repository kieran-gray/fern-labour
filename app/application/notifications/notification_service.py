import logging

from app.application.notifications.entity import Notification
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    NotificationGateway,
    SMSNotificationGateway,
)
from app.domain.subscriber.enums import ContactMethod

log = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        email_notification_gateway: EmailNotificationGateway,
        sms_notification_gateway: SMSNotificationGateway,
    ):
        self._email_notification_gateway = email_notification_gateway
        self._sms_notification_gateway = sms_notification_gateway

    def _get_notification_gateway(self, notification_type: ContactMethod) -> NotificationGateway:
        if notification_type is ContactMethod.EMAIL:
            return self._email_notification_gateway
        elif notification_type is ContactMethod.SMS:
            return self._sms_notification_gateway
        else:
            raise NotImplementedError(
                f"Notification gateway for type {notification_type.value} not implemented"
            )

    async def send(self, notification: Notification) -> None:
        await self._get_notification_gateway(notification.type).send(notification.to_dict())
