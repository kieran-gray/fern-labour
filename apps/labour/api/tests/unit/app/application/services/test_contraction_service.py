from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fern_labour_core.unit_of_work import UnitOfWork

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.domain.domain_event.repository import DomainEventRepository
from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.services.contraction_service import ContractionService
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.contraction.exceptions import ContractionIdInvalid
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.repository import LabourRepository
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.exceptions import (
    UserDoesNotHaveActiveLabour,
)
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "bp_id"
OTHER_USER = "test_id"


@pytest_asyncio.fixture
def event_producer():
    return AsyncMock()


@pytest_asyncio.fixture
async def contraction_service(
    labour_repo: LabourRepository,
    user_service: UserQueryService,
    domain_event_repo: DomainEventRepository,
    unit_of_work: UnitOfWork,
    domain_event_publisher: DomainEventPublisher,
) -> ContractionService:
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
    return ContractionService(
        labour_repository=labour_repo,
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        domain_event_publisher=domain_event_publisher,
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    return await labour_service.begin_labour(BIRTHING_PERSON)


async def test_can_start_contraction(
    contraction_service: ContractionService, labour: LabourDTO
) -> None:
    await contraction_service.start_contraction(labour.birthing_person_id)


async def test_starting_contraction_begins_labour(
    contraction_service: ContractionService, labour_service: LabourService
) -> None:
    labour = await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    labour = await contraction_service.start_contraction(labour.birthing_person_id)
    assert labour.current_phase == LabourPhase.EARLY.value


async def test_cannot_start_contraction_for_non_existent_user(
    contraction_service: ContractionService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await contraction_service.start_contraction("TEST123456")


async def test_can_end_contraction(
    contraction_service: ContractionService, labour: LabourDTO
) -> None:
    await contraction_service.start_contraction(labour.birthing_person_id)
    await contraction_service.end_contraction(labour.birthing_person_id, intensity=5)


async def test_can_update_contraction(
    contraction_service: ContractionService, labour: LabourDTO
) -> None:
    await contraction_service.start_contraction(labour.birthing_person_id)
    labour = await contraction_service.end_contraction(labour.birthing_person_id, intensity=5)

    new_start_time = datetime(2020, 1, 1, 1, 1, tzinfo=UTC)
    new_end_time = datetime(2020, 1, 1, 1, 2, 30, tzinfo=UTC)

    labour = await contraction_service.update_contraction(
        labour.birthing_person_id,
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


async def test_cannot_update_contraction_without_labour(
    contraction_service: ContractionService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await contraction_service.update_contraction(BIRTHING_PERSON, "test", intensity=2)


async def test_cannot_update_contraction_with_invalid_id(
    contraction_service: ContractionService, labour: LabourDTO
) -> None:
    with pytest.raises(ContractionIdInvalid):
        await contraction_service.update_contraction(labour.birthing_person_id, "test", intensity=2)


async def test_can_delete_contraction(
    contraction_service: ContractionService, labour: LabourDTO
) -> None:
    await contraction_service.start_contraction(labour.birthing_person_id)
    labour = await contraction_service.end_contraction(labour.birthing_person_id, intensity=5)

    assert len(labour.contractions) == 1
    labour = await contraction_service.delete_contraction(
        labour.birthing_person_id,
        labour.contractions[0].id,
    )
    assert len(labour.contractions) == 0


async def test_cannot_delete_contraction_without_labour(
    contraction_service: ContractionService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await contraction_service.delete_contraction(BIRTHING_PERSON, "test")


async def test_cannot_delete_contraction_with_invalid_id(
    contraction_service: ContractionService, labour: LabourDTO
) -> None:
    with pytest.raises(ContractionIdInvalid):
        await contraction_service.delete_contraction(labour.birthing_person_id, "test")


async def test_cannot_end_contraction_for_non_existent_user(
    contraction_service: ContractionService,
) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await contraction_service.end_contraction("TEST123456", intensity=5)
