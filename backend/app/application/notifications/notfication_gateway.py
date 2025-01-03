from typing import Any, Protocol


class NotificationGateway(Protocol):
    """Abstract Base Class for notification gateways."""

    async def send(self, data: dict[str, Any]) -> None:
        """
        Send a notification.

        Args:
            data: The data to send
        """


class EmailNotificationGateway(NotificationGateway): ...


class SMSNotificationGateway(NotificationGateway): ...
