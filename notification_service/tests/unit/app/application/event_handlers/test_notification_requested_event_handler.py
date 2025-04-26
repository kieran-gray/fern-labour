import pytest

from src.notification.application.dtos.notification_data import ContactUsData
from src.notification.application.event_handlers.notification_requested_event_handler import (
    NotificationRequestedEventHandler,
)
from src.notification.domain.enums import NotificationChannel, NotificationTemplate
from src.notification.domain.events import NotificationRequested, NotificationRequestedData


@pytest.fixture
def notification_requested_event_handler(notification_service) -> NotificationRequestedEventHandler:
    return NotificationRequestedEventHandler(notification_service=notification_service)


async def test_can_handle_notification_requested_event(
    notification_requested_event_handler: NotificationRequestedEventHandler,
) -> None:
    event_data = NotificationRequestedData(
        channel=NotificationChannel.EMAIL.value,
        destination="email@test.com",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="email@test.com", name="first last", message="message", user_id=""
        ).to_dict(),
    )
    event = NotificationRequested.create(data=event_data.to_dict())
    await notification_requested_event_handler.handle(event=event.to_dict())
