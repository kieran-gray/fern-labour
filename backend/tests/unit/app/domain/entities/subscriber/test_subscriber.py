import pytest

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.exceptions import SubscriberCannotSubscribeToSelf


def test_subscriber_cannot_subscribe_to_self():
    subscriber = Subscriber.create(
        id="test", first_name="User", last_name="Name", contact_methods=["sms"]
    )

    with pytest.raises(SubscriberCannotSubscribeToSelf):
        subscriber.subscribe_to(BirthingPersonId("test"))
