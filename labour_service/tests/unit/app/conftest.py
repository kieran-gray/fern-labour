from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.labour.domain.contraction.entity import Contraction
from src.labour.domain.contraction.value_objects.contraction_duration import Duration
from src.labour.domain.contraction.value_objects.contraction_id import ContractionId
from src.setup.settings import Settings
from tests.unit.app.setup.config.conftest import MockConfigReader


@pytest.fixture
def mock_settings(mock_config_reader: MockConfigReader) -> Settings:
    return Settings.from_file(reader=mock_config_reader)


def get_contractions(
    labour_id: str,
    number_of_contractions: int,
    length_of_contractions: int,
    time_between_contractions: int | float,
    start_time: datetime = datetime(2020, 1, 1, 1, 0, tzinfo=UTC),
) -> list[Contraction]:
    contractions = []
    next_contraction_start = start_time
    for _ in range(number_of_contractions):
        start_time = next_contraction_start
        end_time = start_time + timedelta(minutes=length_of_contractions)
        contractions.append(
            Contraction(
                id_=ContractionId(uuid4()),
                duration=Duration(start_time=start_time, end_time=end_time),
                labour_id=labour_id,
                intensity=5,
            )
        )
        next_contraction_start = end_time + timedelta(minutes=time_between_contractions)
    return contractions
