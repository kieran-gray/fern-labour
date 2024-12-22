from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.contraction.entity import Contraction
from app.domain.contraction.vo_contraction_duration import Duration
from app.domain.contraction.vo_contraction_id import ContractionId
from app.domain.labour.constants import (
    CONTRACTIONS_REQUIRED_NULLIPAROUS,
    CONTRACTIONS_REQUIRED_PAROUS,
    LENGTH_OF_CONTRACTIONS_MINUTES,
    TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    TIME_BETWEEN_CONTRACTIONS_PAROUS,
)
from app.domain.labour.entity import Labour
from app.domain.services.should_go_to_hospital import ShouldGoToHospitalService


@pytest.fixture
def labour() -> Labour:
    return Labour.begin(
        labour_id=UUID("12345678-1234-5678-1234-567812345678"),
        birthing_person_id=BirthingPersonId("87654321-4321-1234-8765-567812345678"),
        start_time=datetime.now(),
        first_labour=True,
    )


def test_should_go_to_hospital_returns_false(labour: Labour):
    assert not ShouldGoToHospitalService().should_go_to_hospital(labour)


def test_should_go_to_hospital_returns_true_parous(labour: Labour):
    contraction_durations = []
    labour.first_labour = False

    next_contraction_start = datetime(2020, 1, 1, 1, 0)
    for _ in range(CONTRACTIONS_REQUIRED_PAROUS):
        start_time = next_contraction_start
        contraction_durations.append(
            Duration(
                start_time=start_time,
                end_time=start_time + timedelta(minutes=LENGTH_OF_CONTRACTIONS_MINUTES),
            )
        )
        next_contraction_start = start_time + timedelta(minutes=TIME_BETWEEN_CONTRACTIONS_PAROUS)

    labour.contractions = [
        Contraction(
            id_=ContractionId(uuid4()), duration=duration, labour_id=labour.id_, intensity=5
        )
        for duration in contraction_durations
    ]
    assert ShouldGoToHospitalService().should_go_to_hospital(labour)


def test_should_go_to_hospital_returns_true_nulliparous(labour: Labour):
    contraction_durations = []

    next_contraction_start = datetime(2020, 1, 1, 1, 0)
    for _ in range(CONTRACTIONS_REQUIRED_NULLIPAROUS):
        start_time = next_contraction_start
        contraction_durations.append(
            Duration(
                start_time=start_time,
                end_time=start_time + timedelta(minutes=LENGTH_OF_CONTRACTIONS_MINUTES),
            )
        )
        next_contraction_start = start_time + timedelta(
            minutes=TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS
        )

    labour.contractions = [
        Contraction(
            id_=ContractionId(uuid4()), duration=duration, labour_id=labour.id_, intensity=5
        )
        for duration in contraction_durations
    ]
    assert ShouldGoToHospitalService().should_go_to_hospital(labour)
