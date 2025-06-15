import logging

import pytest

from src.notification.application.event_handlers.notification_status_updated_event_handler import (
    NotificationStatusUpdatedEventHandler,
)
from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.notification.domain.enums import NotificationChannel, NotificationStatus
from src.notification.domain.events import NotificationStatusUpdated, NotificationStatusUpdatedData


@pytest.fixture
def notification_status_updated_event_handler(
    notification_delivery_service: NotificationDeliveryService,
) -> NotificationStatusUpdatedEventHandler:
    return NotificationStatusUpdatedEventHandler(
        notification_delivery_service=notification_delivery_service
    )


async def test_can_handle_notification_status_updated_event(
    notification_status_updated_event_handler: NotificationStatusUpdatedEventHandler,
    caplog: pytest.LogCaptureFixture,
) -> None:
    event_data = NotificationStatusUpdatedData(
        notification_id="test",
        channel=NotificationChannel.SMS.value,
        from_status=NotificationStatus.SENT,
        to_status=NotificationStatus.SUCCESS,
        external_id="EXT123",
    )
    event = NotificationStatusUpdated.create(aggregate_id="test", aggregate_type="notification", data=event_data.to_dict())
    with caplog.at_level(level=logging.INFO):
        await notification_status_updated_event_handler.handle(event=event.to_dict())

    assert "Redacting notification body for notification ID" in caplog.text


async def test_does_not_redact_notification_email(
    notification_status_updated_event_handler: NotificationStatusUpdatedEventHandler,
    caplog: pytest.LogCaptureFixture,
) -> None:
    event_data = NotificationStatusUpdatedData(
        notification_id="test",
        channel=NotificationChannel.EMAIL.value,
        from_status=NotificationStatus.SENT,
        to_status=NotificationStatus.SUCCESS,
        external_id="EXT123",
    )
    event = NotificationStatusUpdated.create(aggregate_id="test", aggregate_type="notification", data=event_data.to_dict())
    with caplog.at_level(level=logging.INFO):
        await notification_status_updated_event_handler.handle(event=event.to_dict())

    assert caplog.text == ""


async def test_does_not_redact_notification_no_external_id(
    notification_status_updated_event_handler: NotificationStatusUpdatedEventHandler,
    caplog: pytest.LogCaptureFixture,
) -> None:
    event_data = NotificationStatusUpdatedData(
        notification_id="test",
        channel=NotificationChannel.SMS.value,
        from_status=NotificationStatus.SENT,
        to_status=NotificationStatus.SUCCESS,
        external_id=None,
    )
    event = NotificationStatusUpdated.create(aggregate_id="test", aggregate_type="notification", data=event_data.to_dict())
    with caplog.at_level(level=logging.INFO):
        await notification_status_updated_event_handler.handle(event=event.to_dict())

    assert caplog.text == ""


async def test_does_not_redact_notification_not_success_status(
    notification_status_updated_event_handler: NotificationStatusUpdatedEventHandler,
    caplog: pytest.LogCaptureFixture,
) -> None:
    event_data = NotificationStatusUpdatedData(
        notification_id="test",
        channel=NotificationChannel.SMS.value,
        from_status=NotificationStatus.CREATED,
        to_status=NotificationStatus.SENT,
        external_id="EXT123",
    )
    event = NotificationStatusUpdated.create(aggregate_id="test", aggregate_type="notification", data=event_data.to_dict())
    with caplog.at_level(level=logging.INFO):
        await notification_status_updated_event_handler.handle(event=event.to_dict())

    assert caplog.text == ""
