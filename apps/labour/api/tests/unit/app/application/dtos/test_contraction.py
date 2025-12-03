import json
from uuid import UUID, uuid4

import pytest

from src.labour.application.dtos.contraction import ContractionDTO
from src.labour.domain.contraction.entity import Contraction
from src.labour.domain.labour.value_objects.labour_id import LabourId


@pytest.fixture
def contraction() -> Contraction:
    return Contraction.start(labour_id=LabourId(uuid4()))


def test_can_convert_to_contraction_dto(contraction: Contraction) -> None:
    dto = ContractionDTO.from_domain(contraction)
    assert UUID(dto.labour_id) == contraction.labour_id.value
    assert dto.start_time == contraction.start_time
    assert dto.end_time == contraction.end_time
    assert dto.intensity == contraction.intensity
    assert dto.notes == contraction.notes
    assert dto.is_active == contraction.is_active


def test_can_convert_contraction_dto_to_dict(contraction: Contraction) -> None:
    dto = ContractionDTO.from_domain(contraction)
    contraction_dict = dto.to_dict()
    json.dumps(contraction_dict)  # Check dict is json serializable
