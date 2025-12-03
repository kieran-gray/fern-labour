from fern_labour_core.events.event_handler import EventHandler
from fern_labour_notifications_shared.enums import NotificationChannel


def has_sent_email(event_handler: EventHandler) -> bool:
    for domain_event, _ in event_handler._domain_event_repository._data.values():
        channel = domain_event.data.get("channel")
        if channel == NotificationChannel.EMAIL.value:
            return True
    return False


def has_sent_sms(event_handler: EventHandler) -> bool:
    for domain_event, _ in event_handler._domain_event_repository._data.values():
        channel = domain_event.data.get("channel")
        if channel == NotificationChannel.SMS.value:
            return True
    return False
