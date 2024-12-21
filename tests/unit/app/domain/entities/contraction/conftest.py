from uuid import UUID

import pytest

from app.domain.contraction.entity import Contraction


@pytest.fixture
def sample_contraction() -> Contraction:
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    intensity: int = 5
    return Contraction.start(
        labour_id=labour_id,
        intensity=intensity,
    )