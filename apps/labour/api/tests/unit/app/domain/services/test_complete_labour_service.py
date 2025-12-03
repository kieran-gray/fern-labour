import pytest

from src.labour.domain.contraction.services.start_contraction import StartContractionService
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.exceptions import (
    CannotCompleteLabourWithActiveContraction,
    LabourAlreadyCompleted,
)
from src.labour.domain.labour.services.begin_labour import BeginLabourService
from src.labour.domain.labour.services.complete_labour import CompleteLabourService


def test_can_complete_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    assert sample_labour.is_active
    CompleteLabourService().complete_labour(sample_labour)
    assert not sample_labour.is_active
    assert sample_labour.current_phase is LabourPhase.COMPLETE


def test_can_complete_labour_with_notes(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    assert sample_labour.is_active
    CompleteLabourService().complete_labour(sample_labour, notes="Test note")
    assert not sample_labour.is_active
    assert sample_labour.notes == "Test note"
    assert sample_labour.current_phase is LabourPhase.COMPLETE


def test_cannot_complete_labour_already_complete(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    CompleteLabourService().complete_labour(sample_labour)
    with pytest.raises(LabourAlreadyCompleted):
        CompleteLabourService().complete_labour(sample_labour)


def test_cannot_complete_labour_with_active_contraction(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(sample_labour, intensity=1)

    with pytest.raises(CannotCompleteLabourWithActiveContraction):
        CompleteLabourService().complete_labour(sample_labour)
