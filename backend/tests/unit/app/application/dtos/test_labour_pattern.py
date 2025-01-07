import json
from typing import Any

import pytest

from app.application.dtos.labour_pattern import LabourPatternDTO


@pytest.fixture
def labour_pattern() -> dict[str, Any]:
    return {
        "average_duration": 1.123,
        "average_intensity": 6,
        "average_interval": 2.41,
        "phase": "active",
    }


def test_can_convert_to_labour_pattern_dto(labour_pattern) -> None:
    dto = LabourPatternDTO.from_domain(labour_pattern)
    assert dto.average_duration == labour_pattern["average_duration"]
    assert dto.average_intensity == labour_pattern["average_intensity"]
    assert dto.average_interval == labour_pattern["average_interval"]
    assert dto.phase == labour_pattern["phase"]


def test_can_convert_labour_pattern_dto_to_dict(labour_pattern) -> None:
    dto = LabourPatternDTO.from_domain(labour_pattern)
    labour_pattern_dict = dto.to_dict()
    json.dumps(labour_pattern_dict)
