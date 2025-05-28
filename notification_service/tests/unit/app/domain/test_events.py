from src.notification.domain.events import (
    NotificationRequestedData,
    NotificationStatusUpdatedData,
)


def test_can_serde_notification_requested_data():
    event = NotificationRequestedData(
        channel="sms", destination="123", template="test", data={}, metadata={}
    )
    event_dict = event.to_dict()
    from_dict = NotificationRequestedData.from_dict(event_dict)
    assert event == from_dict


def test_can_serde_notification_status_updated_data():
    event = NotificationStatusUpdatedData(
        notification_id="123456",
        channel="sms",
        from_status="sent",
        to_status="delivered",
        external_id="EXT123",
    )
    event_dict = event.to_dict()
    from_dict = NotificationStatusUpdatedData.from_dict(event_dict)
    assert event == from_dict
