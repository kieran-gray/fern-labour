from app.application.events.event_handler import EventHandler
from app.application.events.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.application.events.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from app.application.events.event_handlers.labour_update_posted_event_handler import (
    LabourUpdatePostedEventHandler,
)

EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "labour.update-posted": LabourUpdatePostedEventHandler,
    "labour.begun": LabourBegunEventHandler,
    "labour.completed": LabourCompletedEventHandler,
}
