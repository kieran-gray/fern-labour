from uuid import UUID

import pytest

from src.labour.domain.contraction.entity import Contraction
from src.labour.domain.labour.value_objects.labour_id import LabourId


@pytest.fixture
def sample_contraction() -> Contraction:
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))
    intensity: int = 5
    return Contraction.start(
        labour_id=labour_id,
        intensity=intensity,
    )
