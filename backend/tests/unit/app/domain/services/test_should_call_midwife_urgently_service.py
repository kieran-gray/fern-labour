from datetime import UTC, datetime
from uuid import UUID

import pytest

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.contraction.constants import (
    CONTRACTION_MAX_IN_10_MINS,
    CONTRACTION_MAX_TIME_SECONDS,
)
from app.domain.labour.entity import Labour
from app.domain.services.should_call_midwife_urgently import ShouldCallMidwifeUrgentlyService
from tests.unit.app.conftest import get_contractions


@pytest.fixture
def labour() -> Labour:
    return Labour.plan(
        labour_id=UUID("12345678-1234-5678-1234-567812345678"),
        birthing_person_id=BirthingPersonId("87654321-4321-1234-8765-567812345678"),
        due_date=datetime.now(UTC),
        first_labour=True,
    )


def test_should_call_midwife_returns_false(labour: Labour):
    assert not ShouldCallMidwifeUrgentlyService().should_call_midwife_urgently(labour)


def test_should_call_midwife_returns_true_contraction_length(labour: Labour):
    contractions = get_contractions(
        labour_id=labour.id_.value,
        number_of_contractions=1,
        length_of_contractions=(CONTRACTION_MAX_TIME_SECONDS / 60) + 1,
        time_between_contractions=0,
    )
    labour.contractions = contractions
    assert ShouldCallMidwifeUrgentlyService().should_call_midwife_urgently(labour)


def test_should_call_midwife_returns_true_contraction_count(labour: Labour):
    contractions = get_contractions(
        labour_id=labour.id_.value,
        number_of_contractions=CONTRACTION_MAX_IN_10_MINS,
        length_of_contractions=1,
        time_between_contractions=0.1,
        start_time=datetime.now(UTC),
    )
    labour.contractions = contractions
    assert ShouldCallMidwifeUrgentlyService().should_call_midwife_urgently(labour)
