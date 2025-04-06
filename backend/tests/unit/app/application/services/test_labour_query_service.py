from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.labour.application.dtos.labour import LabourDTO
from app.labour.application.services.labour_query_service import LabourQueryService
from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.exceptions import InvalidLabourId
from app.labour.domain.labour.repository import LabourRepository
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.user.domain.exceptions import (
    UserDoesNotHaveActiveLabour,
)
from app.user.domain.value_objects.user_id import UserId
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
async def labour_query_service(labour_repo: LabourRepository) -> LabourQueryService:
    return LabourQueryService(labour_repository=labour_repo)


async def test_can_get_active_labour(labour_query_service: LabourQueryService) -> None:
    await labour_query_service.get_active_labour(BIRTHING_PERSON_IN_LABOUR)


async def test_cannot_get_active_labour_for_non_existent_birthing_person(
    labour_query_service: LabourQueryService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_query_service.get_active_labour("TEST123456")


async def test_cannot_get_active_labour_for_birthing_person_without_active_labour(
    labour_query_service: LabourQueryService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_query_service.get_active_labour(BIRTHING_PERSON)


async def test_can_get_active_labour_summary(labour_query_service: LabourQueryService) -> None:
    await labour_query_service.get_active_labour_summary(BIRTHING_PERSON_IN_LABOUR)


async def test_cannot_get_active_labour_summary_for_non_existent_birthing_person(
    labour_query_service: LabourQueryService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_query_service.get_active_labour_summary("TEST123456")


async def test_cannot_get_active_labour_summary_for_birthing_person_without_active_labour(
    labour_query_service: LabourQueryService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_query_service.get_active_labour_summary(BIRTHING_PERSON)


async def test_invalid_labour_id_raises_error(labour_query_service: LabourQueryService) -> None:
    with pytest.raises(InvalidLabourId):
        await labour_query_service.get_labour_by_id("test")


async def test_can_get_all_labours(labour_query_service: LabourQueryService) -> None:
    response = await labour_query_service.get_all_labours(BIRTHING_PERSON_IN_LABOUR)
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], LabourDTO)
