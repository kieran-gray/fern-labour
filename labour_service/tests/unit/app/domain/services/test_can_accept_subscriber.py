import pytest

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.exceptions import (
    CannotSubscribeToOwnLabour,
    LabourAlreadyCompleted,
)
from src.labour.domain.labour.services.can_accept_subscriber import CanAcceptSubscriberService
from src.user.domain.value_objects.user_id import UserId


def test_cannot_subscribe_to_own_labour(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    subscriber_id = sample_labour.birthing_person_id

    with pytest.raises(CannotSubscribeToOwnLabour):
        service.can_accept_subscriber(sample_labour, subscriber_id)


def test_cannot_subscribe_to_completed_labour(sample_labour: Labour):
    service = CanAcceptSubscriberService()
    labour = sample_labour
    labour.set_labour_phase(LabourPhase.COMPLETE)

    with pytest.raises(LabourAlreadyCompleted):
        service.can_accept_subscriber(sample_labour, UserId("test"))
