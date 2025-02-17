import json

from app.application.dtos.labour_summary import LabourSummaryDTO
from app.domain.labour.entity import Labour


def test_can_convert_to_labour_summary_dto(sample_labour: Labour) -> None:
    dto = LabourSummaryDTO.from_domain(sample_labour)
    assert dto.id == str(sample_labour.id_.value)
    assert dto.duration == 0.0
    assert dto.contraction_count == len(sample_labour.contractions)
    assert not dto.hospital_recommended
    assert dto.current_phase == sample_labour.current_phase.value
    assert dto.statistics


def test_can_convert_labour_summary_dto_to_dict(sample_labour: Labour) -> None:
    dto = LabourSummaryDTO.from_domain(sample_labour)
    bp_dict = dto.to_dict()
    json.dumps(bp_dict)
