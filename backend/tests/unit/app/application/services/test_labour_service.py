from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from app.application.dtos.labour import LabourDTO
from app.application.events.producer import EventProducer
from app.application.services.labour_service import LabourService
from app.application.services.user_service import UserService
from app.domain.contraction.exceptions import ContractionIdInvalid
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import InvalidLabourUpdateId, LabourUpdateNotFoundById
from app.domain.labour.repository import LabourRepository
from app.domain.user.entity import User
from app.domain.user.exceptions import (
    UserDoesNotHaveActiveLabour,
    UserHasActiveLabour,
    UserNotFoundById,
)
from app.domain.user.vo_user_id import UserId

BIRTHING_PERSON = "bp_id"


@pytest_asyncio.fixture
def event_producer():
    return AsyncMock()


@pytest_asyncio.fixture
async def labour_service(
    labour_repo: LabourRepository,
    user_service: UserService,
    event_producer: EventProducer,
) -> LabourService:
    user_service._user_repository._data = {
        BIRTHING_PERSON: User(
            id_=UserId(BIRTHING_PERSON),
            username="test123",
            first_name="Name",
            last_name="User",
            email="test@email.com",
        )
    }
    return LabourService(
        user_service=user_service,
        labour_repository=labour_repo,
        event_producer=event_producer,
    )


async def test_can_plan_labour(labour_service: LabourService) -> None:
    labour = await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    assert isinstance(labour, LabourDTO)


async def test_can_update_labour_plan(labour_service: LabourService) -> None:
    labour = await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    assert isinstance(labour, LabourDTO)
    assert labour.first_labour

    labour = await labour_service.update_labour_plan(BIRTHING_PERSON, False, labour.due_date)
    assert not labour.first_labour


async def test_cannot_plan_labour_for_non_existent_user(labour_service: LabourService) -> None:
    with pytest.raises(UserNotFoundById):
        await labour_service.plan_labour("TEST123456", True, datetime.now(UTC))


async def test_cannot_update_labour_plan_for_non_existent_user(
    labour_service: LabourService,
) -> None:
    with pytest.raises(UserNotFoundById):
        await labour_service.update_labour_plan("TEST123456", True, datetime.now(UTC))


async def test_cannot_plan_labour_already_has_labour(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    with pytest.raises(UserHasActiveLabour):
        await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))


async def test_cannot_update_labour_plan_has_no_labour(labour_service: LabourService) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.update_labour_plan(BIRTHING_PERSON, True, datetime.now(UTC))


async def test_can_begin_labour(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)


async def test_cannot_begin_unplanned_labour(labour_service: LabourService) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.begin_labour(BIRTHING_PERSON)


async def test_can_complete_labour(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.complete_labour(BIRTHING_PERSON)


async def test_cannot_complete_labour_for_non_existent_user(labour_service: LabourService) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.complete_labour("TEST123456")


async def test_can_start_contraction(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.start_contraction(BIRTHING_PERSON)


async def test_starting_contraction_begins_labour(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    labour = await labour_service.start_contraction(BIRTHING_PERSON)
    assert labour.current_phase == LabourPhase.EARLY.value


async def test_cannot_start_contraction_for_non_existent_user(
    labour_service: LabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.start_contraction("TEST123456")


async def test_can_end_contraction(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.start_contraction(BIRTHING_PERSON)
    await labour_service.end_contraction(BIRTHING_PERSON, intensity=5)


async def test_can_update_contraction(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.start_contraction(BIRTHING_PERSON)
    labour = await labour_service.end_contraction(BIRTHING_PERSON, intensity=5)

    new_start_time = datetime(2020, 1, 1, 1, 1, tzinfo=UTC)
    new_end_time = datetime(2020, 1, 1, 1, 2, 30, tzinfo=UTC)

    labour = await labour_service.update_contraction(
        BIRTHING_PERSON,
        labour.contractions[0].id,
        start_time=new_start_time,
        end_time=new_end_time,
        intensity=2,
        notes="test update",
    )

    contraction = labour.contractions[0]
    assert contraction.duration == 90
    assert contraction.intensity == 2
    assert contraction.notes == "test update"
    assert contraction.start_time == new_start_time
    assert contraction.end_time == new_end_time


async def test_cannot_update_contraction_without_labour(labour_service: LabourService) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.update_contraction(BIRTHING_PERSON, "test", intensity=2)


async def test_cannot_update_contraction_with_invalid_id(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    with pytest.raises(ContractionIdInvalid):
        await labour_service.update_contraction(BIRTHING_PERSON, "test", intensity=2)


async def test_cannot_end_contraction_for_non_existent_user(labour_service: LabourService) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.end_contraction("TEST123456", intensity=5)


async def test_can_post_labour_update(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.start_contraction(BIRTHING_PERSON)
    await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="announcement", message="Test message"
    )


async def test_cannot_post_labour_update_for_non_existent_user(
    labour_service: LabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.post_labour_update(
            "TEST123456", labour_update_type="announcement", message="Test message"
        )


async def test_can_delete_labour_update(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    labour = await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="announcement", message="Test message"
    )
    labour_update = labour.announcements[0]
    await labour_service.delete_labour_update(BIRTHING_PERSON, labour_update_id=labour_update.id)


async def test_cannot_delete_labour_update_for_non_existent_user(
    labour_service: LabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.delete_labour_update(BIRTHING_PERSON, labour_update_id="test")


async def test_cannot_delete_labour_update_with_invalid_id(
    labour_service: LabourService,
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="announcement", message="Test message"
    )
    with pytest.raises(InvalidLabourUpdateId):
        await labour_service.delete_labour_update(BIRTHING_PERSON, labour_update_id="test")


async def test_cannot_delete_labour_update_not_found(
    labour_service: LabourService,
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="announcement", message="Test message"
    )
    with pytest.raises(LabourUpdateNotFoundById):
        await labour_service.delete_labour_update(BIRTHING_PERSON, labour_update_id=str(uuid4()))
