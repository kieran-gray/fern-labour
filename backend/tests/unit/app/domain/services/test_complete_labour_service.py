import pytest

from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import CannotCompleteLabourWithActiveContraction, LabourAlreadyCompleted
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.complete_labour import CompleteLabourService
from app.domain.services.start_contraction import StartContractionService


def test_can_complete_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    assert sample_labour.is_active
    CompleteLabourService().complete_labour(sample_labour)
    assert not sample_labour.is_active
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
