from uuid import UUID

import pytest
from datetime import datetime

from app.domain.contraction.entity import Contraction


@pytest.fixture
def sample_contraction() -> Contraction:
    session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    intensity: int = 5
    return Contraction.start(
        labor_session_id=session_id,
        intensity=intensity,
    )