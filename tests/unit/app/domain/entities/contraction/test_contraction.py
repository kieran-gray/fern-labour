from uuid import UUID
from datetime import datetime

import pytest

from app.domain.contraction.constants import CONTRACTION_MIN_TIME, CONTRACTION_MAX_INTENSITY
from app.domain.contraction.entity import Contraction
from app.domain.contraction.exceptions import ContractionStartTimeAfterEndTime, ContractionIntensityInvalid
from app.domain.contraction.vo_contraction_id import ContractionId
from app.domain.contraction.vo_contraction_duration import Duration

def test_contraction_init():
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    contraction_id: UUID = UUID("87654321-1234-5678-1234-567812345678")
    start_time: datetime = datetime.now()
    intensity: int = 1

    vo_contraction_id = ContractionId(contraction_id)

    direct_contraction = Contraction(
        id_=vo_contraction_id,
        duration=Duration(start_time=start_time, end_time=start_time),
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
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    intensity: int = 1

    contraction = Contraction.start(labour_id=labour_id, intensity=intensity)
    assert isinstance(contraction, Contraction)
    assert isinstance(contraction.duration, Duration)
    assert contraction.is_active


def test_can_end_contraction(sample_contraction: Contraction):
    sample_contraction.end(datetime.now() + CONTRACTION_MIN_TIME)


def test_cannot_init_contraction_with_invalid_intensity():
    labour_id: UUID = UUID("12345678-1234-5678-1234-567812345678")

    with pytest.raises(ContractionIntensityInvalid):
        Contraction.start(
            labour_id=labour_id, intensity=CONTRACTION_MAX_INTENSITY + 1
        )

def test_cannot_update_contraction_to_invalid_intensity(sample_contraction: Contraction):
    with pytest.raises(ContractionIntensityInvalid):
        sample_contraction.update_intensity(CONTRACTION_MAX_INTENSITY + 1)


def test_cannot_end_contraction_before_start_time(sample_contraction: Contraction):
    with pytest.raises(ContractionStartTimeAfterEndTime):
        sample_contraction.end(sample_contraction.start_time - CONTRACTION_MIN_TIME)
