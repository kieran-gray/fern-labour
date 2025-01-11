from typing import Protocol

from app.application.notifications.entity import Notification


class NotificationGateway(Protocol):
    """Abstract Base Class for notification gateways."""

    async def send(self, notification: Notification) -> None:
        """
        Send a notification.

        Args:
            notification: The notification to send
        """


class EmailNotificationGateway(NotificationGateway): ...


class SMSNotificationGateway(NotificationGateway): ...
