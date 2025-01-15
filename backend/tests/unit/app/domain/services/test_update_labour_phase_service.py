from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.contraction.entity import Contraction
from app.domain.labour.enums import LabourPhase
from app.domain.labour.vo_labour_id import LabourId
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.update_labour_phase import UpdateLabourPhaseService


def generate_contractions(length: float, intensity: int) -> list[Contraction]:
    contraction_list = []
    last_start_time = None
    for _ in range(5):
        start_time = last_start_time or datetime.now(UTC)
        end_time = start_time + timedelta(minutes=length)

        contraction = Contraction.start(labour_id=LabourId(uuid4()), start_time=start_time)
        contraction.end(end_time=end_time, intensity=intensity)

        contraction_list.append(contraction)
        last_start_time = start_time

    return contraction_list


@pytest.mark.parametrize(
    "contraction_length,contraction_intensity,expected_labour_phase",
    [
        (0.5, 6, LabourPhase.EARLY),
        (0.99, 6, LabourPhase.EARLY),
        (1, 6, LabourPhase.ACTIVE),
        (1.49, 8, LabourPhase.ACTIVE),
        (1.5, 8, LabourPhase.TRANSITION),
    ],
)
def test_labour_phase_update(
    sample_birthing_person: BirthingPerson,
    contraction_length: float,
    contraction_intensity: int,
    expected_labour_phase: LabourPhase,
):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    sample_birthing_person.active_labour.contractions = generate_contractions(
        length=contraction_length, intensity=contraction_intensity
    )

    assert sample_birthing_person.active_labour.current_phase is LabourPhase.EARLY
    UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)
    assert sample_birthing_person.active_labour.current_phase is expected_labour_phase


def test_labour_phase_no_active_labour(sample_birthing_person: BirthingPerson):
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)


def test_labour_phase_does_not_decrease_from_active(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    sample_birthing_person.active_labour.contractions = generate_contractions(length=1, intensity=6)
    UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)
    assert sample_birthing_person.active_labour.current_phase is LabourPhase.ACTIVE

    sample_birthing_person.active_labour.contractions.extend(
        generate_contractions(length=0.5, intensity=6)
    )

    UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)
    assert sample_birthing_person.active_labour.current_phase is LabourPhase.ACTIVE


@pytest.mark.parametrize("contraction_length,contraction_intensity", [(0.5, 6), (1, 6)])
def test_labour_phase_does_not_decrease_from_transition(
    sample_birthing_person: BirthingPerson, contraction_length: float, contraction_intensity: int
):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    sample_birthing_person.active_labour.contractions = generate_contractions(
        length=1.5, intensity=8
    )
    UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)
    assert sample_birthing_person.active_labour.current_phase is LabourPhase.TRANSITION

    sample_birthing_person.active_labour.contractions.extend(
        generate_contractions(length=contraction_length, intensity=contraction_intensity)
    )

    UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)
    assert sample_birthing_person.active_labour.current_phase is LabourPhase.TRANSITION


@pytest.mark.parametrize("contraction_length,contraction_intensity", [(0.5, 6), (1, 6)])
def test_labour_phase_does_not_decrease_from_pushing(
    sample_birthing_person: BirthingPerson, contraction_length: float, contraction_intensity: int
):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    sample_birthing_person.active_labour.set_labour_phase(LabourPhase.PUSHING)

    sample_birthing_person.active_labour.contractions = generate_contractions(
        length=contraction_length, intensity=contraction_intensity
    )

    UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)
    assert sample_birthing_person.active_labour.current_phase is LabourPhase.PUSHING


@pytest.mark.parametrize("contraction_length,contraction_intensity", [(0.5, 6), (1, 6)])
def test_labour_phase_does_not_decrease_from_complete(
    sample_birthing_person: BirthingPerson, contraction_length: float, contraction_intensity: int
):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    sample_birthing_person.active_labour.set_labour_phase(LabourPhase.COMPLETE)

    sample_birthing_person.active_labour.contractions = generate_contractions(
        length=contraction_length, intensity=contraction_intensity
    )

    UpdateLabourPhaseService().update_labour_phase(sample_birthing_person)
    assert sample_birthing_person.active_labour.current_phase is LabourPhase.COMPLETE
