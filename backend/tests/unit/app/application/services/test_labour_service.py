from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from app.common.infrastructure.events.interfaces.producer import EventProducer
from app.labour.application.dtos.labour import LabourDTO
from app.labour.application.services.labour_service import LabourService
from app.labour.domain.contraction.exceptions import ContractionIdInvalid
from app.labour.domain.labour.enums import LabourPaymentPlan, LabourPhase
from app.labour.domain.labour.exceptions import (
    CannotDeleteActiveLabour,
    InsufficientLabourPaymentPlan,
    InvalidLabourId,
    InvalidLabourPaymentPlan,
    InvalidLabourUpdateId,
    LabourAlreadyCompleted,
    LabourNotFoundById,
    LabourUpdateNotFoundById,
    UnauthorizedLabourRequest,
)
from app.labour.domain.labour.repository import LabourRepository
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.user.application.services.user_service import UserService
from app.user.domain.entity import User
from app.user.domain.exceptions import (
    UserDoesNotHaveActiveLabour,
    UserHasActiveLabour,
    UserNotFoundById,
)
from app.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "bp_id"
OTHER_USER = "test_id"


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


async def test_can_delete_contraction(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.start_contraction(BIRTHING_PERSON)
    labour = await labour_service.end_contraction(BIRTHING_PERSON, intensity=5)

    assert len(labour.contractions) == 1
    labour = await labour_service.delete_contraction(
        BIRTHING_PERSON,
        labour.contractions[0].id,
    )
    assert len(labour.contractions) == 0


async def test_cannot_delete_contraction_without_labour(labour_service: LabourService) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.delete_contraction(BIRTHING_PERSON, "test")


async def test_cannot_delete_contraction_with_invalid_id(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    with pytest.raises(ContractionIdInvalid):
        await labour_service.delete_contraction(BIRTHING_PERSON, "test")


async def test_cannot_end_contraction_for_non_existent_user(labour_service: LabourService) -> None:
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.end_contraction("TEST123456", intensity=5)


async def test_cannot_post_labour_update_incorrect_payment_plan(
    labour_service: LabourService,
) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.start_contraction(BIRTHING_PERSON)
    with pytest.raises(InsufficientLabourPaymentPlan):
        await labour_service.post_labour_update(
            BIRTHING_PERSON, labour_update_type="announcement", message="Test message"
        )


async def test_can_post_labour_update(labour_service: LabourService) -> None:
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY
    )
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
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY
    )
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
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY
    )
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
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY
    )
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


async def test_can_update_labour_payment_plan(labour_service: LabourService):
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    labour = await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.SOLO.value
    )
    assert labour.payment_plan == LabourPaymentPlan.SOLO.value


async def test_cannot_update_labour_payment_plan_of_completed_labour(labour_service: LabourService):
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    await labour_service.begin_labour(BIRTHING_PERSON)
    await labour_service.complete_labour(BIRTHING_PERSON)
    with pytest.raises(LabourAlreadyCompleted):
        await labour_service.update_labour_payment_plan(
            birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.SOLO.value
        )


async def test_cannot_update_labour_payment_plan_non_existent_labour(labour_service: LabourService):
    with pytest.raises(UserDoesNotHaveActiveLabour):
        await labour_service.update_labour_payment_plan(
            birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.SOLO.value
        )


async def test_cannot_update_labour_payment_plan_invalid_id(labour_service: LabourService):
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    with pytest.raises(InvalidLabourPaymentPlan):
        await labour_service.update_labour_payment_plan(
            birthing_person_id=BIRTHING_PERSON, payment_plan="test"
        )


async def test_check_can_update_labour_payment_plan(labour_service: LabourService):
    labour = await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    labour = await labour_service.can_update_labour_payment_plan(
        requester_id=BIRTHING_PERSON, labour_id=labour.id, payment_plan=LabourPaymentPlan.SOLO.value
    )
    assert labour.payment_plan is None


async def test_check_can_update_labour_payment_plan_invalid_labour_id(
    labour_service: LabourService,
):
    await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))

    with pytest.raises(InvalidLabourId):
        await labour_service.can_update_labour_payment_plan(
            requester_id=BIRTHING_PERSON,
            labour_id="test",
            payment_plan=LabourPaymentPlan.SOLO.value,
        )


async def test_check_can_update_labour_payment_plan_invalid_payment_plan(
    labour_service: LabourService,
):
    labour = await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))

    with pytest.raises(InvalidLabourPaymentPlan):
        await labour_service.can_update_labour_payment_plan(
            requester_id=BIRTHING_PERSON, labour_id=labour.id, payment_plan="test"
        )


async def test_check_can_update_labour_payment_plan_non_existent_labour(
    labour_service: LabourService,
):
    with pytest.raises(LabourNotFoundById):
        await labour_service.can_update_labour_payment_plan(
            requester_id=BIRTHING_PERSON,
            labour_id=str(uuid4()),
            payment_plan=LabourPaymentPlan.SOLO.value,
        )


async def test_check_can_update_labour_payment_plan_unauthorised(labour_service: LabourService):
    labour = await labour_service.plan_labour(BIRTHING_PERSON, True, datetime.now(UTC))
    with pytest.raises(UnauthorizedLabourRequest):
        await labour_service.can_update_labour_payment_plan(
            requester_id="different_id",
            labour_id=labour.id,
            payment_plan=LabourPaymentPlan.SOLO.value,
        )
