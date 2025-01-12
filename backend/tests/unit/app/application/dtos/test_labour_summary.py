import json

import pytest

from app.application.dtos.labour_summary import LabourSummaryDTO
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour


@pytest.fixture
def labour() -> Labour:
    return Labour.begin(birthing_person_id=BirthingPersonId("test"), first_labour=True)


def test_can_convert_to_labour_summary_dto(labour: Labour) -> None:
    dto = LabourSummaryDTO.from_domain(labour)
    assert dto.id == str(labour.id_.value)
    assert dto.duration
    assert dto.contraction_count == len(labour.contractions)
    assert not dto.hospital_recommended
    assert dto.current_phase == labour.current_phase.value
    assert dto.statistics


def test_can_convert_labour_summary_dto_to_dict(labour: Labour) -> None:
    dto = LabourSummaryDTO.from_domain(labour)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
