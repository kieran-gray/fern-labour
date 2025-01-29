from app.application.events.event_handler import EventHandler
from app.application.events.event_handlers.birthing_person_removed_subscriber_event_handler import (
    BirthingPersonRemovedSubscriberEventHandler,
)
from app.application.events.event_handlers.birthing_person_send_invite_event_handler import (
    BirthingPersonSendInviteEventHandler,
)
from app.application.events.event_handlers.contact_us_message_sent_event_handler import (
    ContactUsMessageSentEventHandler,
)
from app.application.events.event_handlers.labour_announcement_made_event_handler import (
    LabourAnnouncementMadeEventHandler,
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

EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "labour.announcement-made": LabourAnnouncementMadeEventHandler,
    "labour.begun": LabourBegunEventHandler,
    "labour.completed": LabourCompletedEventHandler,
    "subscriber.subscribed-to": SubscriberSubscribedToEventHandler,
    "subscriber.unsubscribed-from": SubscriberUnsubscribedFromEventHandler,
    "birthing-person.removed-subscriber": BirthingPersonRemovedSubscriberEventHandler,
    "birthing-person.send-invite": BirthingPersonSendInviteEventHandler,
    "contact-us.message-sent": ContactUsMessageSentEventHandler,
}
