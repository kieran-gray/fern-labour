from unittest.mock import AsyncMock
from datetime import datetime, UTC

import pytest
import pytest_asyncio

from app.application.dtos.labour import LabourDTO
from app.application.events.producer import EventProducer
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.labour_service import LabourService
from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour, BirthingPersonHasActiveLabour, BirthingPersonNotFoundById
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.enums import LabourPhase
from app.domain.labour.repository import LabourRepository
from tests.unit.app.application.conftest import MockBirthingPersonRepository

BIRTHING_PERSON = "bp_id"


@pytest_asyncio.fixture
def event_producer():
    return AsyncMock()


@pytest_asyncio.fixture
async def labour_service(
    labour_repo: LabourRepository,
    birthing_person_service: BirthingPersonService,
    event_producer: EventProducer,
) -> LabourService:
    birthing_person_service._birthing_person_repository._data = {
        BIRTHING_PERSON: BirthingPerson(
            id_=BirthingPersonId(BIRTHING_PERSON),
            first_name="Name",
            last_name="User",
            labours=[],
        )
    }
    return LabourService(
        birthing_person_service=birthing_person_service,
        labour_repository=labour_repo,
        event_producer=event_producer,
    )


async def test_can_plan_labour(labour_service: LabourService) -> None:
    labour = await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    assert isinstance(labour, LabourDTO)


async def test_cannot_plan_labour_for_non_existent_user(labour_service: LabourService) -> None:
    with pytest.raises(BirthingPersonNotFoundById):
        await labour_service.plan_labour("TEST123456", True, datetime.now(UTC))


async def test_cannot_plan_labour_already_has_labour(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    with pytest.raises(BirthingPersonHasActiveLabour):
        await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))


async def test_can_begin_labour(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)


async def test_cannot_begin_unplanned_labour(labour_service: LabourService) -> None:
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        await labour_service.begin_labour(BIRTHING_PERSON)


async def test_can_complete_labour(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.complete_labour(BIRTHING_PERSON)


async def test_cannot_complete_labour_for_non_existent_user(labour_service: LabourService) -> None:
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
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
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        await labour_service.start_contraction("TEST123456")


async def test_can_end_contraction(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.start_contraction(BIRTHING_PERSON)
    await labour_service.end_contraction(BIRTHING_PERSON, intensity=5)


async def test_cannot_end_contraction_for_non_existent_user(labour_service: LabourService) -> None:
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
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
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        await labour_service.post_labour_update(
            "TEST123456", labour_update_type="announcement", message="Test message"
        )
