from fern_labour_core.events.event_handler import EventHandler

from src.labour.application.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from src.labour.application.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from src.labour.application.event_handlers.labour_update_posted_event_handler import (
    LabourUpdatePostedEventHandler,
)

LABOUR_EVENT_HANDLER_MAPPING: dict[str, type[EventHandler]] = {
    "labour.update-posted": LabourUpdatePostedEventHandler,
    "labour.begun": LabourBegunEventHandler,
    "labour.completed": LabourCompletedEventHandler,
}
