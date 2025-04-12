from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.labour.application.dtos.labour import LabourDTO
from app.labour.application.security.labour_authorization_service import LabourAuthorizationService
from app.labour.application.services.labour_service import LabourService
from app.labour.domain.labour.exceptions import UnauthorizedLabourRequest

BIRTHING_PERSON = "bp_id"


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    return await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )


async def test_ensure_can_access_labour_authorized(labour: LabourDTO):
    service = LabourAuthorizationService()
    await service.ensure_can_access_labour(BIRTHING_PERSON, labour)


async def test_ensure_can_access_labour_unauthorized(labour: LabourDTO):
    service = LabourAuthorizationService()

    with pytest.raises(UnauthorizedLabourRequest):
        await service.ensure_can_access_labour("someone-else", labour)
