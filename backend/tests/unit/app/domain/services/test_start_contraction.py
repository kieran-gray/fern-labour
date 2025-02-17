import pytest

from app.domain.labour.entity import Labour
from app.domain.labour.exceptions import LabourAlreadyCompleted, LabourHasActiveContraction
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.complete_labour import CompleteLabourService
from app.domain.services.start_contraction import StartContractionService


def test_can_start_contraction(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(sample_labour)


def test_cannot_start_multiple_contractions(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(sample_labour)
    with pytest.raises(LabourHasActiveContraction):
        StartContractionService().start_contraction(sample_labour)


def test_cannot_start_contraction_for_completed_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    CompleteLabourService().complete_labour(sample_labour)
    with pytest.raises(LabourAlreadyCompleted):
        StartContractionService().start_contraction(sample_labour)
