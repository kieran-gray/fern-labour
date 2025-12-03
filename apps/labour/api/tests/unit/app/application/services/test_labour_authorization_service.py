from datetime import UTC, datetime

import pytest
import pytest_asyncio

from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.security.labour_authorization_service import LabourAuthorizationService
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.exceptions import InvalidLabourId, UnauthorizedLabourRequest
from src.labour.domain.labour.repository import LabourRepository

BIRTHING_PERSON = "bp_id"


@pytest_asyncio.fixture
async def labour_authorization_service(labour_repo: LabourRepository) -> LabourAuthorizationService:
    return LabourAuthorizationService(labour_repository=labour_repo)


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    return await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )


async def test_ensure_can_access_labour_authorized(
    labour_authorization_service: LabourAuthorizationService, labour: LabourDTO
):
    await labour_authorization_service.ensure_can_access_labour(BIRTHING_PERSON, labour.id)


async def test_ensure_can_access_labour_unauthorized(
    labour_authorization_service: LabourAuthorizationService, labour: LabourDTO
):
    with pytest.raises(UnauthorizedLabourRequest):
        await labour_authorization_service.ensure_can_access_labour("someone-else", labour.id)


async def test_checking_for_authorization_with_invalid_id_raises_error(
    labour_authorization_service: LabourAuthorizationService,
):
    with pytest.raises(InvalidLabourId):
        await labour_authorization_service.ensure_can_access_labour("someone-else", "test")
