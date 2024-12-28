import json

import pytest

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.domain.birthing_person.entity import BirthingPerson


@pytest.fixture
def birthing_person() -> BirthingPerson:
    return BirthingPerson.create(
        birthing_person_id="test",
        first_name="User",
        last_name="Name",
        first_labour=True,
    )


def test_can_convert_to_birthing_person_dto(birthing_person: BirthingPerson) -> None:
    dto = BirthingPersonDTO.from_domain(birthing_person)
    assert dto.id == birthing_person.id_.value
    assert dto.first_name == birthing_person.first_name
    assert dto.last_name == birthing_person.last_name
    assert dto.labours == birthing_person.labours
    assert dto.subscribers == birthing_person.subscribers


def test_can_convert_birthing_person_dto_to_dict(birthing_person: BirthingPerson) -> None:
    dto = BirthingPersonDTO.from_domain(birthing_person)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
