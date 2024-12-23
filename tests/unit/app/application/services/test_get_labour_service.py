from copy import deepcopy
from datetime import datetime

import pytest
import pytest_asyncio
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

from app.domain.labour.entity import Labour
from app.domain.labour.vo_labour_id import LabourId
from app.application.services.get_labour_service import GetLabourService
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import (
    BirthingPersonDoesNotHaveActiveLabour,
    BirthingPersonNotFoundById,
)
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId

BIRTHING_PERSON = "bp_id"
BIRTHING_PERSON_IN_LABOUR = "bp_2_id"

class MockBirthingPersonRepository(BirthingPersonRepository):
    _data = {}
    _initial_data = {
        BIRTHING_PERSON: BirthingPerson(
            id_=BirthingPersonId(BIRTHING_PERSON), name="Name User", first_labour=True, labours=[]
        ),
        BIRTHING_PERSON_IN_LABOUR: BirthingPerson(
            id_=BirthingPersonId(BIRTHING_PERSON_IN_LABOUR),
            name="User Name",
            first_labour=True,
            labours=[
                Labour(
                    id_=LabourId("test"),
                    birthing_person_id=BirthingPersonId(BIRTHING_PERSON_IN_LABOUR),
                    start_time=datetime.now(),
                    first_labour=True
                )
            ]
        )
    }

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
    container = make_async_container(
        MockBirthingPersonRepositoryProvider(),
    )
    yield container
    await container.close()


@pytest_asyncio.fixture
async def birthing_person_repo(container: AsyncContainer):
    repo = await container.get(BirthingPersonRepository)
    repo.reset()
    return repo


@pytest_asyncio.fixture
async def get_labour_service(birthing_person_repo: BirthingPersonRepository) -> GetLabourService:
    return GetLabourService(birthing_person_repository=birthing_person_repo)


async def test_can_get_active_labour(get_labour_service: GetLabourService) -> None:
    await get_labour_service.get_active_labour(BIRTHING_PERSON_IN_LABOUR)


async def test_cannot_get_active_labour_for_non_existent_birthing_person(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(BirthingPersonNotFoundById):
        await get_labour_service.get_active_labour("TEST123456")


async def test_cannot_get_active_labour_for_birthing_person_without_active_labour(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        await get_labour_service.get_active_labour(BIRTHING_PERSON)


async def test_can_get_active_labour_summary(get_labour_service: GetLabourService) -> None:
    await get_labour_service.get_active_labour_summary(BIRTHING_PERSON_IN_LABOUR)


async def test_cannot_get_active_labour_summary_for_non_existent_birthing_person(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(BirthingPersonNotFoundById):
        await get_labour_service.get_active_labour_summary("TEST123456")


async def test_cannot_get_active_labour_summary_for_birthing_person_without_active_labour(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        await get_labour_service.get_active_labour_summary(BIRTHING_PERSON)
