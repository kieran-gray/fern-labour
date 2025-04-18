from src.core.application.event_handler import EventHandler
from src.notification.application.event_handlers.notification_requested_event_handler import (
    NotificationRequestedEventHandler,
)

NOTIFICATION_EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "notification.requested": NotificationRequestedEventHandler,
}
