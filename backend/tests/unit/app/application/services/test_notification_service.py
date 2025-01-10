from enum import StrEnum

import pytest
import pytest_asyncio

from app.application.notifications.entity import Notification
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
)
from app.application.notifications.notification_service import NotificationService
from app.domain.subscriber.enums import ContactMethod


class MockEmailNotificationGateway(EmailNotificationGateway):
    sent_notifications = []

    async def send(self, data: Notification) -> None:
        self.sent_notifications.append(data)


class MockSMSNotificationGateway(SMSNotificationGateway):
    sent_notifications = []

    async def send(self, data: Notification) -> None:
        self.sent_notifications.append(data)


@pytest_asyncio.fixture
def email_notification_gateway():
    return MockEmailNotificationGateway()


@pytest_asyncio.fixture
def sms_notification_gateway():
    return MockSMSNotificationGateway()


@pytest_asyncio.fixture
async def notification_service(
    email_notification_gateway: EmailNotificationGateway,
    sms_notification_gateway: SMSNotificationGateway,
) -> NotificationService:
    email_notification_gateway.sent_notifications = []
    sms_notification_gateway.sent_notifications = []
    return NotificationService(
        email_notification_gateway=email_notification_gateway,
        sms_notification_gateway=sms_notification_gateway,
    )


async def test_can_send_email(notification_service: NotificationService) -> None:
    notification: Notification = Notification(
        type=ContactMethod.EMAIL, message="test message", destination="dest", subject="test subject"
    )
    await notification_service.send(notification)
    assert notification_service._sms_notification_gateway.sent_notifications == []
    assert notification_service._email_notification_gateway.sent_notifications == [notification]


async def test_can_send_sms(notification_service: NotificationService) -> None:
    notification: Notification = Notification(
        type=ContactMethod.SMS,
        message="test message",
        destination="dest",
    )
    await notification_service.send(notification)
    assert notification_service._sms_notification_gateway.sent_notifications == [notification]
    assert notification_service._email_notification_gateway.sent_notifications == []


async def test_invalid_type_raises_not_implemented(
    notification_service: NotificationService,
) -> None:
    class ContactMethod(StrEnum):
        TEST = "test"

    notification: Notification = Notification(
        type=ContactMethod.TEST, message="test message", destination="dest", subject="test subject"
    )
    with pytest.raises(NotImplementedError):
        await notification_service.send(notification)
