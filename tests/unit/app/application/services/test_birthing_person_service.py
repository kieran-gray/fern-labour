from copy import deepcopy

import pytest
import pytest_asyncio
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.application.services.birthing_person_service import BirthingPersonService
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import (
    BirthingPersonExistsWithID,
    BirthingPersonNotFoundById,
)
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId


class MockBirthingPersonRepository(BirthingPersonRepository):
    _data = {}
    _initial_data = {}

    def reset(self) -> None:
        self._data = deepcopy(self._initial_data)

    async def save(self, birthing_person: BirthingPerson) -> None:
        self._data[birthing_person.id_.value] = birthing_person

    async def delete(self, birthing_person: BirthingPerson) -> None:
        self._data.pop(birthing_person.id_.value)

    async def get_by_id(self, birthing_person_id: BirthingPersonId) -> BirthingPerson | None:
        return self._data.get(birthing_person_id.value, None)


class MockBirthingPersonRepositoryProvider(Provider):
    scope = Scope.APP

    @provide
    def get_birthing_person_repository(self) -> BirthingPersonRepository:
        return MockBirthingPersonRepository()


@pytest_asyncio.fixture
async def container():
    container = make_async_container(MockBirthingPersonRepositoryProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture
async def birthing_person_repo(container: AsyncContainer):
    repo = await container.get(BirthingPersonRepository)
    repo.reset()
    return repo


@pytest_asyncio.fixture
async def birthing_person_service(
    birthing_person_repo: BirthingPersonRepository,
) -> BirthingPersonService:
    return BirthingPersonService(birthing_person_repo)


async def test_register_birthing_person(birthing_person_service: BirthingPersonService):
    birthing_person = await birthing_person_service.register("test", "User Name", True)
    assert isinstance(birthing_person, BirthingPersonDTO)
    assert birthing_person.id == "test"
    assert birthing_person.name == "User Name"
    assert birthing_person.first_labour is True
    assert birthing_person.labours == []
    assert birthing_person.contacts == []


async def test_cannot_register_multiple_birthing_persons_with_same_id(
    birthing_person_service: BirthingPersonService,
):
    await birthing_person_service.register("test", "User Name", True)
    with pytest.raises(BirthingPersonExistsWithID):
        await birthing_person_service.register("test", "User Name", True)


async def test_can_add_contact(birthing_person_service: BirthingPersonService):
    birthing_person_id = "test"
    birthing_person: BirthingPersonDTO = await birthing_person_service.register(
        birthing_person_id, "User Name", True
    )

    assert birthing_person.contacts == []

    birthing_person = await birthing_person_service.add_contact(
        birthing_person_id,
        name="Contact Name",
        phone_number="07123123123",
        email="test@email.com",
        contact_methods=[],
    )
    assert birthing_person.contacts != []
    contact = birthing_person.contacts[0]
    assert contact.name == "Contact Name"
    assert contact.phone_number == "07123123123"
    assert contact.email == "test@email.com"
    assert contact.contact_methods == []


async def test_cannot_add_contact_to_non_existent_birthing_person(
    birthing_person_service: BirthingPersonService,
):
    with pytest.raises(BirthingPersonNotFoundById):
        await birthing_person_service.add_contact(
            "123",
            name="Contact Name",
            phone_number="07123123123",
            email="test@email.com",
            contact_methods=[],
        )


async def test_get_birthing_person(birthing_person_service: BirthingPersonService):
    birthing_person_id = "test"
    await birthing_person_service.register(birthing_person_id, "User Name", True)
    birthing_person = await birthing_person_service.get_birthing_person(birthing_person_id)

    assert isinstance(birthing_person, BirthingPersonDTO)


async def test_cannot_get_non_existent_birthing_person(
    birthing_person_service: BirthingPersonService,
):
    with pytest.raises(BirthingPersonNotFoundById):
        await birthing_person_service.get_birthing_person("test")
