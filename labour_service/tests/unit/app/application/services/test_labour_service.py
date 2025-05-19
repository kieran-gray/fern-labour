from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fern_labour_core.events.producer import EventProducer

from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.exceptions import InvalidLabourUpdateRequest
from src.labour.application.services.contraction_service import ContractionService
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.exceptions import (
    CannotDeleteActiveLabour,
    InvalidLabourId,
    InvalidLabourUpdateId,
    LabourNotFoundById,
    LabourUpdateNotFoundById,
    UnauthorizedLabourRequest,
)
from src.labour.domain.labour.repository import LabourRepository
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.labour.domain.labour_update.exceptions import CannotUpdateLabourUpdate
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.exceptions import (
    UserDoesNotHaveActiveLabour,
    UserHasActiveLabour,
)
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "bp_id"
OTHER_USER = "test_id"


@pytest_asyncio.fixture
def event_producer():
    return AsyncMock()


@pytest_asyncio.fixture
async def labour_service(
    labour_repo: LabourRepository,
    user_service: UserQueryService,
    event_producer: EventProducer,
) -> LabourService:
    user_service._user_repository._data = {
        BIRTHING_PERSON: User(
            id_=UserId(BIRTHING_PERSON),
            username="test123",
            first_name="Name",
            last_name="User",
            email="test@email.com",
        ),
        OTHER_USER: User(
            id_=UserId(OTHER_USER),
            username="abc123",
            first_name="Test",
            last_name="Smith",
            email="test@smith.com",
        ),
    }
    return LabourService(
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


async def test_cannot_update_labour_plan_for_non_existent_user(
    labour_service: LabourService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
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


async def test_can_post_labour_update(
    labour_service: LabourService, contraction_service: ContractionService
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await contraction_service.start_contraction(BIRTHING_PERSON)
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
    labour_update = labour.labour_updates[0]
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


async def test_can_delete_labour(labour_service: LabourService):
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    labour = await labour_service.complete_labour(BIRTHING_PERSON)
    await labour_service.delete_labour(BIRTHING_PERSON, labour_id=labour.id)

    assert not await labour_service._labour_repository.get_by_id(labour_id=LabourId(labour.id))


async def test_cannot_delete_labour_in_progress(labour_service: LabourService):
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    labour = await labour_service.begin_labour(BIRTHING_PERSON)

    with pytest.raises(CannotDeleteActiveLabour):
        await labour_service.delete_labour(BIRTHING_PERSON, labour_id=labour.id)


async def test_cannot_delete_labour_not_own(labour_service: LabourService):
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    labour = await labour_service.begin_labour(BIRTHING_PERSON)

    with pytest.raises(UnauthorizedLabourRequest):
        await labour_service.delete_labour(OTHER_USER, labour_id=labour.id)


async def test_cannot_delete_labour_does_not_exist(labour_service: LabourService):
    with pytest.raises(LabourNotFoundById):
        await labour_service.delete_labour(BIRTHING_PERSON, labour_id=str(uuid4()))


async def test_cannot_delete_labour_invalid_id(labour_service: LabourService):
    with pytest.raises(InvalidLabourId):
        await labour_service.delete_labour(OTHER_USER, labour_id="test123")


async def test_can_update_labour_update_message(
    labour_service: LabourService, contraction_service: ContractionService
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await contraction_service.start_contraction(BIRTHING_PERSON)
    labour = await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="status_update", message="Test message"
    )
    labour_update = labour.labour_updates[-1]
    await labour_service.update_labour_update(
        BIRTHING_PERSON, labour_update_id=labour_update.id, message="New message"
    )


async def test_cannot_update_labour_begun_message(
    labour_service: LabourService, contraction_service: ContractionService
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await contraction_service.start_contraction(BIRTHING_PERSON)
    labour = await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="status_update", message="Test message"
    )
    labour_update = labour.labour_updates[0]
    with pytest.raises(CannotUpdateLabourUpdate):
        await labour_service.update_labour_update(
            BIRTHING_PERSON, labour_update_id=labour_update.id, message="New message"
        )


async def test_can_update_labour_update_type(
    labour_service: LabourService, contraction_service: ContractionService
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await contraction_service.start_contraction(BIRTHING_PERSON)
    labour = await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="status_update", message="Test message"
    )
    labour_update = labour.labour_updates[0]
    await labour_service.update_labour_update(
        BIRTHING_PERSON, labour_update_id=labour_update.id, labour_update_type="announcement"
    )


async def test_must_update_message_or_type(
    labour_service: LabourService, contraction_service: ContractionService
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await contraction_service.start_contraction(BIRTHING_PERSON)
    labour = await labour_service.post_labour_update(
        BIRTHING_PERSON, labour_update_type="status_update", message="Test message"
    )
    labour_update = labour.labour_updates[0]
    with pytest.raises(InvalidLabourUpdateRequest):
        await labour_service.update_labour_update(
            BIRTHING_PERSON, labour_update_id=labour_update.id
        )


async def test_cannot_update_labour_update_invalid_id(
    labour_service: LabourService, contraction_service: ContractionService
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await contraction_service.start_contraction(BIRTHING_PERSON)
    with pytest.raises(InvalidLabourUpdateId):
        await labour_service.update_labour_update(
            BIRTHING_PERSON, labour_update_id="should fail", message="New message"
        )
