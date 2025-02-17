import json
from uuid import UUID, uuid4

import pytest

from app.application.dtos.labour_update import LabourUpdateDTO
from app.domain.labour.vo_labour_id import LabourId
from app.domain.labour_update.entity import LabourUpdate
from app.domain.labour_update.enums import LabourUpdateType


@pytest.fixture
def labour_update() -> LabourUpdate:
    return LabourUpdate.create(
        labour_update_type=LabourUpdateType.STATUS_UPDATE,
        labour_id=LabourId(uuid4()),
        message="Test Message",
    )


def test_can_convert_to_labour_update_dto(labour_update: LabourUpdate) -> None:
    dto = LabourUpdateDTO.from_domain(labour_update)
    assert UUID(dto.labour_id) == labour_update.labour_id.value
    assert dto.sent_time == labour_update.sent_time
    assert dto.message == labour_update.message
    assert UUID(dto.id) == labour_update.id_.value


def test_can_convert_labour_update_dto_to_dict(labour_update: LabourUpdate) -> None:
    dto = LabourUpdateDTO.from_domain(labour_update)
    labour_update_dict = dto.to_dict()
    json.dumps(labour_update_dict)  # Check dict is json serializable
