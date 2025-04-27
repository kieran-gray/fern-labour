from src.notification.events import NotificationRequestedData


def test_can_serde_notification_requested_data():
    event = NotificationRequestedData(
        channel="sms", destination="123", template="test", data={}, metadata={}
    )
    event_dict = event.to_dict()
    from_dict = NotificationRequestedData.from_dict(event_dict)
    assert event == from_dict
