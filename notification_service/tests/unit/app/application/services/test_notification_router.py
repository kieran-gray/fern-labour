import pytest

from src.notification.application.services.notification_router import NotificationRouter
from src.notification.domain.enums import NotificationChannel
from src.notification.domain.exceptions import InvalidNotificationChannel
from tests.unit.app.application.conftest import MockEmailNotificationGateway


async def test_missing_router_raises_not_implemented() -> None:
    router = NotificationRouter()
    with pytest.raises(NotImplementedError):
        router.get_gateway(NotificationChannel.EMAIL.value)


async def test_invalid_channel_raises_error() -> None:
    router = NotificationRouter()
    with pytest.raises(InvalidNotificationChannel):
        router.get_gateway("test")


async def test_can_register_gateway() -> None:
    router = NotificationRouter()
    router.register_gateway(NotificationChannel.EMAIL.value, MockEmailNotificationGateway())
    assert isinstance(router.get_gateway(NotificationChannel.EMAIL), MockEmailNotificationGateway)
