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
