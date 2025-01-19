import pytest

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.application.dtos.birthing_person_summary import BirthingPersonSummaryDTO
from app.application.services.birthing_person_service import BirthingPersonService
from app.domain.birthing_person.exceptions import (
    BirthingPersonExistsWithID,
    BirthingPersonNotFoundById,
)
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.vo_subscriber_id import SubscriberId


async def test_register_birthing_person(birthing_person_service: BirthingPersonService):
    birthing_person = await birthing_person_service.register("test", "User", "Name")
    assert isinstance(birthing_person, BirthingPersonDTO)
    assert birthing_person.id == "test"
    assert birthing_person.first_name == "User"
    assert birthing_person.last_name == "Name"
    assert birthing_person.labours == []


async def test_cannot_register_multiple_birthing_persons_with_same_id(
    birthing_person_service: BirthingPersonService,
):
    await birthing_person_service.register("test", "User", "Name")
    with pytest.raises(BirthingPersonExistsWithID):
        await birthing_person_service.register("test", "User", "Name")


async def test_get_birthing_person(birthing_person_service: BirthingPersonService):
    birthing_person_id = "test"
    await birthing_person_service.register(birthing_person_id, "User", "Name")
    birthing_person = await birthing_person_service.get_birthing_person(birthing_person_id)

    assert isinstance(birthing_person, BirthingPersonDTO)
    assert birthing_person.first_name == "User"
    assert birthing_person.last_name == "Name"


async def test_cannot_get_non_existent_birthing_person(
    birthing_person_service: BirthingPersonService,
):
    with pytest.raises(BirthingPersonNotFoundById):
        await birthing_person_service.get_birthing_person("test")


async def test_get_birthing_person_summary(birthing_person_service: BirthingPersonService):
    birthing_person_id = "test"
    await birthing_person_service.register(birthing_person_id, "User", "Name")
    birthing_person = await birthing_person_service.get_birthing_person_summary(birthing_person_id)

    assert isinstance(birthing_person, BirthingPersonSummaryDTO)
    assert birthing_person.first_name == "User"
    assert birthing_person.last_name == "Name"


async def test_cannot_get_summary_for_non_existent_birthing_person(
    birthing_person_service: BirthingPersonService,
):
    with pytest.raises(BirthingPersonNotFoundById):
        await birthing_person_service.get_birthing_person_summary("test")


async def test_can_remove_subscriber(birthing_person_service: BirthingPersonService):
    birthing_person_id = "test"
    subscriber_id = SubscriberId("test123")
    await birthing_person_service.register(birthing_person_id, "User", "Name")
    birthing_person = await birthing_person_service._birthing_person_repository.get_by_id(
        BirthingPersonId(birthing_person_id)
    )
    birthing_person.add_subscriber(subscriber_id)
    await birthing_person_service._birthing_person_repository.save(birthing_person)

    birthing_person_dto = await birthing_person_service.get_birthing_person(birthing_person_id)
    assert birthing_person.subscribers == [subscriber_id]

    await birthing_person_service.remove_subscriber(birthing_person_id, subscriber_id.value)
    birthing_person_dto = await birthing_person_service.get_birthing_person(birthing_person_id)
    assert birthing_person_dto.subscribers == []
