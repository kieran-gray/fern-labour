from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.application.dtos.labour import LabourDTO
from app.application.services.get_labour_service import GetLabourService
from app.domain.labour.entity import Labour
from app.domain.labour.exceptions import InvalidLabourId
from app.domain.labour.repository import LabourRepository
from app.domain.labour.vo_labour_id import LabourId
from app.domain.user.exceptions import (
    UserDoesNotHaveActiveLabour,
)
from app.domain.user.vo_user_id import UserId
from tests.unit.app.application.conftest import MockLabourRepository

BIRTHING_PERSON = "bp_id"
BIRTHING_PERSON_IN_LABOUR = "bp_2_id"


@pytest_asyncio.fixture
async def labour_repo():
    repo = MockLabourRepository()
    repo._data = {
        "test": Labour(
            id_=LabourId("test"),
            birthing_person_id=UserId(BIRTHING_PERSON_IN_LABOUR),
            due_date=datetime.now(UTC),
            first_labour=True,
        ),
    }
    return repo


@pytest_asyncio.fixture
async def get_labour_service(labour_repo: LabourRepository) -> GetLabourService:
    return GetLabourService(labour_repository=labour_repo)


async def test_can_get_active_labour(get_labour_service: GetLabourService) -> None:
    await get_labour_service.get_active_labour(BIRTHING_PERSON_IN_LABOUR)


async def test_cannot_get_active_labour_for_non_existent_birthing_person(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await get_labour_service.get_active_labour("TEST123456")


async def test_cannot_get_active_labour_for_birthing_person_without_active_labour(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await get_labour_service.get_active_labour(BIRTHING_PERSON)


async def test_can_get_active_labour_summary(get_labour_service: GetLabourService) -> None:
    await get_labour_service.get_active_labour_summary(BIRTHING_PERSON_IN_LABOUR)


async def test_cannot_get_active_labour_summary_for_non_existent_birthing_person(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await get_labour_service.get_active_labour_summary("TEST123456")


async def test_cannot_get_active_labour_summary_for_birthing_person_without_active_labour(
    get_labour_service: GetLabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await get_labour_service.get_active_labour_summary(BIRTHING_PERSON)


async def test_invalid_labour_id_raises_error(get_labour_service: GetLabourService) -> None:
    with pytest.raises(InvalidLabourId):
        await get_labour_service.get_labour_by_id("test")


async def test_can_get_all_labours(get_labour_service: GetLabourService) -> None:
    response = await get_labour_service.get_all_labours(BIRTHING_PERSON_IN_LABOUR)
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], LabourDTO)
