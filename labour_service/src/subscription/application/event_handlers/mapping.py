from fern_labour_core.events.event_handler import EventHandler

from src.subscription.application.event_handlers.subscriber_approved_event_handler import (
    SubscriberApprovedEventHandler,
)
from src.subscription.application.event_handlers.subscriber_requested_event_handler import (
    SubscriberRequestedEventHandler,
)

SUBSCRIPTION_EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "subscriber.requested": SubscriberRequestedEventHandler,
    "subscriber.approved": SubscriberApprovedEventHandler,
}
