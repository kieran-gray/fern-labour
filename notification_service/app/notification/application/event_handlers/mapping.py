from app.common.application.event_handler import EventHandler
from app.notification.application.event_handlers.notification_requested_event_handler import (
    NotificationRequestedEventHandler,
)

NOTIFICATION_EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "notification.requested": NotificationRequestedEventHandler,
}
