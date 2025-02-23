import json

import pytest

from app.application.dtos.birthing_person_summary import BirthingPersonSummaryDTO
from app.domain.birthing_person.entity import BirthingPerson


@pytest.fixture
def birthing_person() -> BirthingPerson:
    return BirthingPerson.create(
        birthing_person_id="test",
        first_name="User",
        last_name="Name",
    )


def test_can_convert_to_birthing_person_summary_dto(birthing_person: BirthingPerson) -> None:
    dto = BirthingPersonSummaryDTO.from_domain(birthing_person)
    assert dto.id == birthing_person.id_.value
    assert dto.first_name == birthing_person.first_name
    assert dto.last_name == birthing_person.last_name


def test_can_convert_birthing_person_summary_dto_to_dict(birthing_person: BirthingPerson) -> None:
    dto = BirthingPersonSummaryDTO.from_domain(birthing_person)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
