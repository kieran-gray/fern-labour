from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.interfaces.notification_gateway import NotificationGateway
from src.notification.domain.enums import NotificationChannel
from src.notification.domain.exceptions import InvalidNotificationChannel


class NotificationRouter:
    def __init__(self) -> None:
        self._gateways: dict[NotificationChannel, NotificationGateway] = {}

    def _channel_to_domain(self, channel: str) -> NotificationChannel:
        try:
            notification_channel = NotificationChannel(channel)
        except ValueError:
            raise InvalidNotificationChannel(notification_channel=channel)
        return notification_channel

    def register_gateway(self, channel: str, gateway: NotificationGateway) -> None:
        """Register a gateway for a specific channel"""
        notification_channel = self._channel_to_domain(channel=channel)
        self._gateways[notification_channel] = gateway

    def get_gateway(self, channel: str) -> NotificationGateway:
        notification_channel = self._channel_to_domain(channel=channel)
        if gateway := self._gateways.get(notification_channel):
            return gateway
        raise NotImplementedError(f"Notification gateway for type {channel} not implemented")

    async def route_notification(self, notification: NotificationDTO) -> NotificationSendResult:
        """Route notification to appropriate gateway based on rules"""
        gateway = self.get_gateway(notification.channel)
        result = await gateway.send(notification)
        return result
