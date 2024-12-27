from abc import ABC, abstractmethod
from typing import Any


class NotificationGateway(ABC):
    """Abstract Base Class for notification gateways."""

    @abstractmethod
    async def send(self, data: dict[str, Any]) -> None:
        """
        Send a notification.

        Args:
            data: The data to send
        """


class EmailNotificationGateway(NotificationGateway):
    pass


class SMSNotificationGateway(NotificationGateway):
    pass
