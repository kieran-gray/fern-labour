from uuid import UUID

from app.domain.labour.entity import Labour
from app.domain.contraction.entity import Contraction
from app.domain.labour.exceptions import LaborSessionCompleted, CannotCompleteLaborSessionWithActiveContraction, LaborSessionHasActiveContraction, LaborSessionHasNoActiveContraction
from app.domain.labour.vo_labour_id import LabourId
from app.domain.contraction.constants import CONTRACTION_MIN_TIME, CONTRACTION_MAX_INTENSITY
from datetime import datetime

import pytest


def test_labor_session_init():
    session_id: UUID = UUID("12345678-1234-5678-1234-567812345678")
    user_id: UUID = UUID("87654321-4321-1234-8765-567812345678")
    start_time: datetime = datetime.now()

    vo_session_id = LabourId(session_id)

    direct_session = Labour(
        id_=vo_session_id,
        birthing_person_id=user_id,
        start_time=start_time,
        first_labor=True,
    )

    indirect_session = Labour.begin(
        session_id=session_id,
        birthing_person_id=user_id,
        first_labor=True,
        start_time=start_time,
    )

    assert isinstance(indirect_session, Labour)
    assert direct_session.id_ == vo_session_id == indirect_session.id_
    assert direct_session == indirect_session


def test_can_start_contraction(sample_labor_session):
    assert sample_labor_session.contractions == []

    sample_labor_session.start_contraction(intensity=CONTRACTION_MAX_INTENSITY)
    assert len(sample_labor_session.contractions) == 1
    assert sample_labor_session.has_active_contraction
    
    active_contraction = sample_labor_session.active_contraction
    assert isinstance(active_contraction, Contraction)


def test_can_end_contraction(sample_labor_session):
    sample_labor_session.start_contraction(intensity=CONTRACTION_MAX_INTENSITY)
    sample_labor_session.end_contraction(datetime.now()+CONTRACTION_MIN_TIME)
    assert len(sample_labor_session.contractions) == 1
    assert not sample_labor_session.has_active_contraction


def test_cannot_start_multiple_contractions(sample_labor_session):
    sample_labor_session.start_contraction(intensity=CONTRACTION_MAX_INTENSITY)
    with pytest.raises(LaborSessionHasActiveContraction):
        sample_labor_session.start_contraction(intensity=CONTRACTION_MAX_INTENSITY)


def test_cannot_end_contraction_that_doesnt_exist(sample_labor_session):
    with pytest.raises(LaborSessionHasNoActiveContraction):
        sample_labor_session.end_contraction()


def test_can_end_labor_session(sample_labor_session):
    sample_labor_session.complete_labor()


def test_cannot_end_labor_session_with_active_contraction(sample_labor_session):
    sample_labor_session.start_contraction(intensity=CONTRACTION_MAX_INTENSITY)
    with pytest.raises(CannotCompleteLaborSessionWithActiveContraction):
        sample_labor_session.complete_labor()


def test_cannot_start_contraction_for_completed_labor(sample_labor_session):
    sample_labor_session.complete_labor()
    with pytest.raises(LaborSessionCompleted):
        sample_labor_session.start_contraction(intensity=CONTRACTION_MAX_INTENSITY)
