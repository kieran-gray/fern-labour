from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.labour.domain.labour.constants import (
    LENGTH_OF_CONTRACTIONS_MINUTES,
    TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    TIME_BETWEEN_CONTRACTIONS_PAROUS,
)
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.services.begin_labour import BeginLabourService
from src.labour.domain.labour.services.should_prepare_for_hospital import (
    ShouldPrepareForHospitalService,
)
from src.user.domain.value_objects.user_id import UserId
from tests.unit.app.conftest import get_contractions


@pytest.fixture
def labour() -> Labour:
    labour = Labour.plan(
        labour_id=UUID("12345678-1234-5678-1234-567812345678"),
        birthing_person_id=UserId("87654321-4321-1234-8765-567812345678"),
        due_date=datetime.now(UTC),
        first_labour=True,
    )
    return BeginLabourService().begin_labour(labour)


def test_should_prepare_for_hospital_returns_false(labour: Labour):
    assert not ShouldPrepareForHospitalService().should_prepare_for_hospital(labour)


def test_should_prepare_for_hospital_returns_true_parous(labour: Labour):
    contractions = get_contractions(
        labour_id=labour.id_.value,
        number_of_contractions=4,
        length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
        time_between_contractions=TIME_BETWEEN_CONTRACTIONS_PAROUS,
    )
    labour.first_labour = False
    labour.contractions = contractions
    assert ShouldPrepareForHospitalService().should_prepare_for_hospital(labour)


def test_should_prepare_for_hospital_returns_true_nulliparous(labour: Labour):
    contractions = get_contractions(
        labour_id=labour.id_.value,
        number_of_contractions=4,
        length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
        time_between_contractions=TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    )
    labour.contractions = contractions
    assert ShouldPrepareForHospitalService().should_prepare_for_hospital(labour)


def test_should_prepare_for_hospital_returns_false_when_contractions_too_far_apart(labour: Labour):
    contractions = get_contractions(
        labour_id=labour.id_.value,
        number_of_contractions=4,
        length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
        time_between_contractions=TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS + 1,
    )

    labour.contractions = contractions
    assert not ShouldPrepareForHospitalService().should_prepare_for_hospital(labour)
