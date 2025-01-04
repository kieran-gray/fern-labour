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
    "labour.begun": LabourBegunEventHandler,
    "labour.completed": LabourCompletedEventHandler,
    "subscriber.subscribed-to": SubscriberSubscribedToEventHandler,
    "subscriber.unsubscribed-from": SubscriberUnsubscribedFromEventHandler,
    "contraction.ended": ContractionEndedEventHandler,
}
