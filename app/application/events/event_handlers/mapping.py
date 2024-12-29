from app.application.events.event_handlers.contraction_ended_event_handler import (
    ContractionEndedEventHandler,
)
from app.application.events.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.application.events.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from app.application.events.event_handlers.subscriber_subscribed_to_event_handler import (
    SubscriberSubscribedToEventHandler,
)
from app.application.events.event_handlers.subscriber_unsubscribed_from_event_handler import (
    SubscriberUnsubscribedFromEventHandler,
)

EVENT_HANDLER_MAPPING = {
    "labour_tracker.labour.begun": LabourBegunEventHandler,
    "labour_tracker.labour.completed": LabourCompletedEventHandler,
    "labour_tracker.subscriber.subscribed-to": SubscriberSubscribedToEventHandler,
    "labour_tracker.subscriber.unsubscribed-from": SubscriberUnsubscribedFromEventHandler,
    "labour_tracker.contraction.ended": ContractionEndedEventHandler,
}
