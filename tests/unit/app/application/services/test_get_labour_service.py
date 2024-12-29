from datetime import datetime

import pytest
import pytest_asyncio

from app.application.services.get_labour_service import GetLabourService
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import (
    BirthingPersonDoesNotHaveActiveLabour,
    BirthingPersonNotFoundById,
)
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour
from app.domain.labour.vo_labour_id import LabourId
from tests.unit.app.application.conftest import MockBirthingPersonRepository

BIRTHING_PERSON = "bp_id"
BIRTHING_PERSON_IN_LABOUR = "bp_2_id"


@pytest_asyncio.fixture
async def birthing_person_repo():
    repo = MockBirthingPersonRepository()
    repo._data = {
        BIRTHING_PERSON: BirthingPerson(
            id_=BirthingPersonId(BIRTHING_PERSON),
            first_name="Name",
            last_name="User",
            labours=[],
        ),
        BIRTHING_PERSON_IN_LABOUR: BirthingPerson(
            id_=BirthingPersonId(BIRTHING_PERSON_IN_LABOUR),
            first_name="User",
            last_name="Name",
            labours=[
                Labour(
                    id_=LabourId("test"),
                    birthing_person_id=BirthingPersonId(BIRTHING_PERSON_IN_LABOUR),
                    start_time=datetime.now(),
                    first_labour=True,
                )
            ],
        ),
    }
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
