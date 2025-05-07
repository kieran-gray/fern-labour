from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.exceptions import (
    CannotSubscribeToOwnLabour,
    LabourAlreadyCompleted,
)
from src.user.domain.value_objects.user_id import UserId


class CanAcceptSubscriberService:
    def can_accept_subscriber(self, labour: Labour, subscriber_id: UserId) -> None:
        if labour.birthing_person_id == subscriber_id:
            raise CannotSubscribeToOwnLabour()
        if labour.current_phase is LabourPhase.COMPLETE:
            raise LabourAlreadyCompleted()
        return
