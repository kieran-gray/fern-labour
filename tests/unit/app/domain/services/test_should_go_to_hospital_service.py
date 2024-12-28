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


def get_contraction_durations(
    number_of_contractions: int, length_of_contractions: int, time_between_contractions: int
) -> list[Duration]:
    contraction_durations = []
    next_contraction_start = datetime(2020, 1, 1, 1, 0)
    for _ in range(number_of_contractions):
        start_time = next_contraction_start
        end_time = start_time + timedelta(minutes=length_of_contractions)
        contraction_durations.append(Duration(start_time=start_time, end_time=end_time))
        next_contraction_start = end_time + timedelta(minutes=time_between_contractions)
    return contraction_durations


def test_should_go_to_hospital_returns_false(labour: Labour):
    assert not ShouldGoToHospitalService().should_go_to_hospital(labour)


def test_should_go_to_hospital_returns_true_parous(labour: Labour):
    contraction_durations = get_contraction_durations(
        number_of_contractions=CONTRACTIONS_REQUIRED_PAROUS,
        length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
        time_between_contractions=TIME_BETWEEN_CONTRACTIONS_PAROUS,
    )
    labour.first_labour = False

    labour.contractions = [
        Contraction(
            id_=ContractionId(uuid4()), duration=duration, labour_id=labour.id_, intensity=5
        )
        for duration in contraction_durations
    ]
    assert ShouldGoToHospitalService().should_go_to_hospital(labour)


def test_should_go_to_hospital_returns_true_nulliparous(labour: Labour):
    contraction_durations = get_contraction_durations(
        number_of_contractions=CONTRACTIONS_REQUIRED_NULLIPAROUS,
        length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
        time_between_contractions=TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    )

    labour.contractions = [
        Contraction(
            id_=ContractionId(uuid4()), duration=duration, labour_id=labour.id_, intensity=5
        )
        for duration in contraction_durations
    ]
    assert ShouldGoToHospitalService().should_go_to_hospital(labour)


def test_should_go_to_hospital_returns_false_when_contractions_too_far_apart(labour: Labour):
    contraction_durations = get_contraction_durations(
        number_of_contractions=CONTRACTIONS_REQUIRED_NULLIPAROUS,
        length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
        time_between_contractions=TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS + 1,
    )

    labour.contractions = [
        Contraction(
            id_=ContractionId(uuid4()), duration=duration, labour_id=labour.id_, intensity=5
        )
        for duration in contraction_durations
    ]
    assert not ShouldGoToHospitalService().should_go_to_hospital(labour)
