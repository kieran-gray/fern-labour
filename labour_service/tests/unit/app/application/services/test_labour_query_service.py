from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.exceptions import (
    InvalidLabourId,
    LabourAlreadyCompleted,
    LabourNotFoundById,
)
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.user.domain.exceptions import (
    UserDoesNotHaveActiveLabour,
)
from src.user.domain.value_objects.user_id import UserId
from tests.unit.app.application.conftest import MockLabourRepository

BIRTHING_PERSON = "bp_id"
BIRTHING_PERSON_IN_LABOUR = "bp_2_id"
LABOUR_ID = UUID("12345678-1234-5678-1234-567812345678")


@pytest_asyncio.fixture
async def labour_query_service() -> LabourQueryService:
    labour_repo = MockLabourRepository()
    labour_repo._data = {
        LABOUR_ID: Labour(
            id_=LabourId(LABOUR_ID),
            birthing_person_id=UserId(BIRTHING_PERSON_IN_LABOUR),
            due_date=datetime.now(UTC),
            first_labour=True,
        ),
    }
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


async def test_can_get_labour_by_id(labour_query_service: LabourQueryService) -> None:
    labour = await labour_query_service.get_labour_by_id(str(LABOUR_ID))
    assert isinstance(labour, LabourDTO)


async def test_invalid_labour_id_raises_error(labour_query_service: LabourQueryService) -> None:
    with pytest.raises(InvalidLabourId):
        await labour_query_service.get_labour_by_id("test")


async def test_can_get_all_labours(labour_query_service: LabourQueryService) -> None:
    response = await labour_query_service.get_all_labours(BIRTHING_PERSON_IN_LABOUR)
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], LabourDTO)


async def test_can_accept_subscriber(labour_query_service: LabourQueryService) -> None:
    result = await labour_query_service.can_accept_subscriber("subscriber", str(LABOUR_ID))
    assert result is None


async def test_cannot_accept_subscriber_invalid_labour_id(
    labour_query_service: LabourQueryService,
) -> None:
    with pytest.raises(InvalidLabourId):
        await labour_query_service.can_accept_subscriber("subscriber", "invalid")


async def test_cannot_accept_subscriber_labour_not_found(
    labour_query_service: LabourQueryService,
) -> None:
    with pytest.raises(LabourNotFoundById):
        await labour_query_service.can_accept_subscriber("subscriber", str(uuid4()))


async def test_ensure_labour_is_active_success(labour_query_service: LabourQueryService) -> None:
    await labour_query_service.ensure_labour_is_active(labour_id=str(LABOUR_ID))


async def test_ensure_labour_is_active_completed(labour_query_service: LabourQueryService) -> None:
    labour = await labour_query_service._labour_repository.get_by_id(LabourId(LABOUR_ID))
    labour.complete_labour()
    await labour_query_service._labour_repository.save(labour)

    with pytest.raises(LabourAlreadyCompleted):
        await labour_query_service.ensure_labour_is_active(labour_id=str(LABOUR_ID))


async def test_ensure_labour_is_active_invalid_id(labour_query_service: LabourQueryService) -> None:
    with pytest.raises(InvalidLabourId):
        await labour_query_service.ensure_labour_is_active(labour_id="test")


async def test_ensure_labour_is_active_not_found(labour_query_service: LabourQueryService) -> None:
    with pytest.raises(LabourNotFoundById):
        await labour_query_service.ensure_labour_is_active(labour_id=str(uuid4()))
