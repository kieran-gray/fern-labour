from fern_labour_core.events.event_handler import EventHandler

from src.notification.application.event_handlers.notification_created_event_handler import (
    NotificationCreatedEventHandler
)
from src.notification.application.event_handlers.notification_requested_event_handler import (
    NotificationRequestedEventHandler,
)
from src.notification.application.event_handlers.notification_status_updated_event_handler import (
    NotificationStatusUpdatedEventHandler,
)

NOTIFICATION_EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "notification.requested": NotificationRequestedEventHandler,
    "notification.created": NotificationCreatedEventHandler,
    "notification.status-updated": NotificationStatusUpdatedEventHandler,
}
