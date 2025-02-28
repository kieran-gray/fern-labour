import pytest

from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import LabourAlreadyCompleted
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.update_labour_phase import UpdateLabourPhaseService
from tests.unit.app.domain.services.conftest import generate_contractions


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
    sample_labour: Labour,
    contraction_length: float,
    contraction_intensity: int,
    expected_labour_phase: LabourPhase,
):
    BeginLabourService().begin_labour(sample_labour)
    sample_labour.contractions = generate_contractions(
        length=contraction_length, intensity=contraction_intensity
    )

    assert sample_labour.current_phase is LabourPhase.EARLY
    UpdateLabourPhaseService().update_labour_phase(sample_labour)
    assert sample_labour.current_phase is expected_labour_phase


def test_labour_phase_does_not_decrease_from_active(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    sample_labour.contractions = generate_contractions(length=1, intensity=6)
    UpdateLabourPhaseService().update_labour_phase(sample_labour)
    assert sample_labour.current_phase is LabourPhase.ACTIVE

    sample_labour.contractions.extend(generate_contractions(length=0.5, intensity=6))

    UpdateLabourPhaseService().update_labour_phase(sample_labour)
    assert sample_labour.current_phase is LabourPhase.ACTIVE


@pytest.mark.parametrize("contraction_length,contraction_intensity", [(0.5, 6), (1, 6)])
def test_labour_phase_does_not_decrease_from_transition(
    sample_labour: Labour, contraction_length: float, contraction_intensity: int
):
    BeginLabourService().begin_labour(sample_labour)
    sample_labour.contractions = generate_contractions(length=1.5, intensity=8)
    UpdateLabourPhaseService().update_labour_phase(sample_labour)
    assert sample_labour.current_phase is LabourPhase.TRANSITION

    sample_labour.contractions.extend(
        generate_contractions(length=contraction_length, intensity=contraction_intensity)
    )

    UpdateLabourPhaseService().update_labour_phase(sample_labour)
    assert sample_labour.current_phase is LabourPhase.TRANSITION


@pytest.mark.parametrize("contraction_length,contraction_intensity", [(0.5, 6), (1, 6)])
def test_labour_phase_does_not_decrease_from_pushing(
    sample_labour: Labour, contraction_length: float, contraction_intensity: int
):
    BeginLabourService().begin_labour(sample_labour)
    sample_labour.set_labour_phase(LabourPhase.PUSHING)

    sample_labour.contractions = generate_contractions(
        length=contraction_length, intensity=contraction_intensity
    )

    UpdateLabourPhaseService().update_labour_phase(sample_labour)
    assert sample_labour.current_phase is LabourPhase.PUSHING


@pytest.mark.parametrize("contraction_length,contraction_intensity", [(0.5, 6), (1, 6)])
def test_labour_phase_does_not_decrease_from_complete(
    sample_labour: Labour, contraction_length: float, contraction_intensity: int
):
    BeginLabourService().begin_labour(sample_labour)
    sample_labour.set_labour_phase(LabourPhase.COMPLETE)

    sample_labour.contractions = generate_contractions(
        length=contraction_length, intensity=contraction_intensity
    )

    with pytest.raises(LabourAlreadyCompleted):
        UpdateLabourPhaseService().update_labour_phase(sample_labour)
    assert sample_labour.current_phase is LabourPhase.COMPLETE
