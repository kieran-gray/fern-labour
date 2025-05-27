from typing import Protocol

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult


class NotificationGateway(Protocol):
    """Abstract Base Class for notification gateways."""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        """
        Send a notification.

        Args:
            notification: The notification to send
        """

    async def get_status(self, external_id: str) -> str:
        """
        Get the status of a sent notification.

        Args:
            external_id: The notification external ID
        """


class EmailNotificationGateway(NotificationGateway, Protocol): ...


class SMSNotificationGateway(NotificationGateway, Protocol): ...


class WhatsAppNotificationGateway(NotificationGateway, Protocol): ...
