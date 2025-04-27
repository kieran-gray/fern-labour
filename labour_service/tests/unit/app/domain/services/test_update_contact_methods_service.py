from uuid import uuid4

import pytest

from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import ContactMethod
from src.subscription.domain.services.update_contact_methods import UpdateContactMethodsService
from src.user.domain.value_objects.user_id import UserId


@pytest.fixture
def sample_subscription() -> Subscription:
    return Subscription.create(
        labour_id=LabourId(uuid4()),
        birthing_person_id=UserId("birthing_person"),
        subscriber_id=UserId("subscriber"),
    )


def test_can_update_contact_methods(sample_subscription: Subscription):
    assert sample_subscription.contact_methods == []
    contact_methods = [ContactMethod.EMAIL]
    subscription = UpdateContactMethodsService().update_contact_methods(
        subscription=sample_subscription, contact_methods=contact_methods
    )
    assert subscription.contact_methods == contact_methods


def test_whatsapp_takes_priority_over_sms(sample_subscription: Subscription):
    assert sample_subscription.contact_methods == []
    contact_methods = [ContactMethod.SMS, ContactMethod.WHATSAPP]
    subscription = UpdateContactMethodsService().update_contact_methods(
        subscription=sample_subscription, contact_methods=contact_methods
    )
    assert subscription.contact_methods == [ContactMethod.WHATSAPP]
