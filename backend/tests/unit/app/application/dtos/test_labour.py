import json

import pytest

from app.application.dtos.labour import LabourDTO
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour


@pytest.fixture
def labour() -> Labour:
    return Labour.begin(birthing_person_id=BirthingPersonId("test"), first_labour=True)


def test_can_convert_to_labour_dto(labour: Labour) -> None:
    dto = LabourDTO.from_domain(labour)
    assert dto.id == str(labour.id_.value)
    assert dto.birthing_person_id == labour.birthing_person_id.value
    assert dto.start_time == labour.start_time
    assert dto.end_time == labour.end_time
    assert dto.current_phase == labour.current_phase.value
    assert dto.notes == labour.notes
    assert dto.contractions == labour.contractions


def test_can_convert_labour_dto_to_dict(labour: Labour) -> None:
    dto = LabourDTO.from_domain(labour)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
