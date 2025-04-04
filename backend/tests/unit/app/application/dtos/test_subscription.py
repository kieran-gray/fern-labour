import json
from uuid import uuid4

import pytest

from app.application.dtos.subscription import SubscriptionDTO
from app.domain.user.vo_user_id import UserId
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.subscription.entity import Subscription
from app.labour.domain.subscription.enums import ContactMethod, SubscriberRole, SubscriptionStatus


@pytest.fixture
def subscription() -> Subscription:
    return Subscription.create(
        labour_id=LabourId(uuid4()),
        birthing_person_id=UserId("test_birthing_person"),
        subscriber_id=UserId("test_subscriber"),
        status=SubscriptionStatus.SUBSCRIBED,
        role=SubscriberRole.BIRTH_PARTNER,
        contact_methods=[ContactMethod.SMS],
    )


def test_can_convert_to_subscription_dto(subscription: Subscription) -> None:
    dto = SubscriptionDTO.from_domain(subscription)
    assert dto.labour_id == str(subscription.labour_id.value)
    assert dto.birthing_person_id == subscription.birthing_person_id.value
    assert dto.subscriber_id == subscription.subscriber_id.value
    assert dto.status == subscription.status
    assert dto.role == subscription.role
    assert dto.contact_methods == subscription.contact_methods


def test_can_convert_subscription_dto_to_dict(subscription: Subscription) -> None:
    dto = SubscriptionDTO.from_domain(subscription)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
