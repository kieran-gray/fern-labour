from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from app.domain.contraction.constants import CONTRACTION_MAX_INTENSITY, CONTRACTION_MIN_TIME_SECONDS
from app.domain.contraction.entity import Contraction
from app.domain.contraction.exceptions import (
    ContractionIntensityInvalid,
    ContractionStartTimeAfterEndTime,
)
from app.domain.contraction.vo_contraction_duration import Duration
from app.domain.contraction.vo_contraction_id import ContractionId
from app.domain.labour.vo_labour_id import LabourId


def test_contraction_init():
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))
    contraction_id: UUID = UUID("87654321-1234-5678-1234-567812345678")
    start_time: datetime = datetime.now(UTC)
    intensity: int = 1

    vo_contraction_id = ContractionId(contraction_id)

    direct_contraction = Contraction(
        id_=vo_contraction_id,
        duration=Duration.create(start_time=start_time, end_time=start_time),
        labour_id=labour_id,
        intensity=intensity,
    )

    indirect_contraction = Contraction.start(
        contraction_id=contraction_id,
        labour_id=labour_id,
        start_time=start_time,
        intensity=intensity,
    )

    assert isinstance(indirect_contraction, Contraction)
    assert direct_contraction.id_ == vo_contraction_id == indirect_contraction.id_
    assert direct_contraction == indirect_contraction


def test_contraction_init_default_values():
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))
    intensity: int = 1

    contraction = Contraction.start(labour_id=labour_id, intensity=intensity)
    assert isinstance(contraction, Contraction)
    assert isinstance(contraction.duration, Duration)
    assert contraction.is_active


def test_can_end_contraction(sample_contraction: Contraction):
    sample_contraction.end(
        datetime.now(UTC) + timedelta(seconds=CONTRACTION_MIN_TIME_SECONDS), intensity=5
    )


def test_cannot_init_contraction_with_invalid_intensity():
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))

    with pytest.raises(ContractionIntensityInvalid):
        Contraction.start(labour_id=labour_id, intensity=CONTRACTION_MAX_INTENSITY + 1)


def test_can_update_contraction_intensity(sample_contraction: Contraction):
    sample_contraction.update_intensity(CONTRACTION_MAX_INTENSITY)


def test_can_set_contraction_notes(sample_contraction: Contraction):
    sample_contraction.add_notes("Test")
    assert sample_contraction.notes == "Test"


def test_cannot_update_contraction_to_invalid_intensity(sample_contraction: Contraction):
    with pytest.raises(ContractionIntensityInvalid):
        sample_contraction.update_intensity(CONTRACTION_MAX_INTENSITY + 1)


def test_cannot_end_contraction_before_start_time(sample_contraction: Contraction):
    with pytest.raises(ContractionStartTimeAfterEndTime):
        sample_contraction.end(
            sample_contraction.start_time - timedelta(seconds=CONTRACTION_MIN_TIME_SECONDS),
            intensity=5,
        )


def test_contraction_duration_str(sample_contraction: Contraction):
    assert str(sample_contraction.duration) == "0m 0s"

    sample_contraction.duration = Duration(
        start_time=datetime(2020, 1, 1, 1, 0), end_time=datetime(2020, 1, 1, 1, 1, 40)
    )
    assert str(sample_contraction.duration) == "1m 40s"
