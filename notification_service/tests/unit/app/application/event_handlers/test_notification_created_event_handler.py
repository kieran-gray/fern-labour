import pytest
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import ContactUsData

from src.notification.application.event_handlers.notification_created_event_handler import NotificationCreatedEventHandler
from src.notification.domain.enums import NotificationChannel
from src.notification.domain.events import NotificationCreated, NotificationCreatedData


@pytest.fixture
def notification_created_event_handler(notification_service) -> NotificationCreatedEventHandler:
    return NotificationCreatedEventHandler(notification_service=notification_service)


async def test_can_handle_notification_created_event(
    notification_created_event_handler: NotificationCreatedEventHandler,
) -> None:
    notification = await notification_created_event_handler._notification_service.create_notification(
        channel=NotificationChannel.EMAIL.value,
        destination="test",
        template=NotificationTemplate.CONTACT_US_SUBMISSION.value,
        data=ContactUsData(
            email="test@email.com", name="test", message="test", user_id="abc123"
        ).to_dict(),
    )

    event_data = NotificationCreatedData(notification_id=notification.id)
    event = NotificationCreated.create(aggregate_id="test", aggregate_type="notification", data=event_data.to_dict())
    await notification_created_event_handler.handle(event=event.to_dict())
