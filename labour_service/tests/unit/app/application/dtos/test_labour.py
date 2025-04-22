import json

from src.labour.application.dtos.labour import LabourDTO
from src.labour.domain.labour.entity import Labour


def test_can_convert_to_labour_dto(sample_labour: Labour) -> None:
    dto = LabourDTO.from_domain(sample_labour)
    assert dto.id == str(sample_labour.id_.value)
    assert dto.birthing_person_id == sample_labour.birthing_person_id.value
    assert dto.due_date == sample_labour.due_date
    assert dto.labour_name == sample_labour.labour_name
    assert dto.start_time == sample_labour.start_time
    assert dto.end_time == sample_labour.end_time
    assert dto.current_phase == sample_labour.current_phase.value
    assert dto.notes == sample_labour.notes
    assert dto.contractions == sample_labour.contractions


def test_can_convert_labour_dto_to_dict(sample_labour: Labour) -> None:
    dto = LabourDTO.from_domain(sample_labour)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
