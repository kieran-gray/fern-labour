from fern_labour_core.events.event_handler import EventHandler

from src.application.event_handlers.contact_message_created_event_handler import (
    ContactMessageCreatedEventHandler,
)

CONTACT_EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "contact-message.created": ContactMessageCreatedEventHandler,
}
