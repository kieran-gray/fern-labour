import json

import pytest

from app.application.dtos.subscriber import SubscriberDTO
from app.domain.subscriber.entity import Subscriber
from app.domain.subscription.enums import ContactMethod


@pytest.fixture
def subscriber() -> Subscriber:
    return Subscriber.create(
        id="test",
        first_name="User",
        last_name="Name",
        phone_number="07123123123",
        email="test@email.com",
    )


def test_can_convert_to_subscriber_dto(subscriber: Subscriber) -> None:
    dto = SubscriberDTO.from_domain(subscriber)
    assert dto.id == subscriber.id_.value
    assert dto.first_name == subscriber.first_name
    assert dto.last_name == subscriber.last_name
    assert dto.phone_number == subscriber.phone_number
    assert dto.email == subscriber.email


def test_can_convert_subscriber_dto_to_dict(subscriber: Subscriber) -> None:
    dto = SubscriberDTO.from_domain(subscriber)
    subscriber_dict = dto.to_dict()
    json.dumps(subscriber_dict)


def test_subscriber_destination(subscriber: Subscriber) -> None:
    dto = SubscriberDTO.from_domain(subscriber)
    assert dto.destination(ContactMethod.SMS.value) == subscriber.phone_number
    assert dto.destination(ContactMethod.EMAIL.value) == subscriber.email


def test_subscriber_destination_returns_none(subscriber: Subscriber) -> None:
    dto = SubscriberDTO.from_domain(subscriber)
    dto.email = None
    dto.phone_number = None
    assert dto.destination(ContactMethod.SMS.value) is None
    assert dto.destination(ContactMethod.EMAIL.value) is None


def test_subscriber_destination_invalid_contact_method(subscriber: Subscriber) -> None:
    dto = SubscriberDTO.from_domain(subscriber)
    with pytest.raises(ValueError):
        dto.destination("test")
