import pytest

from app.labour.domain.contraction.constants import CONTRACTION_MAX_INTENSITY
from app.labour.domain.contraction.services.end_contraction import EndContractionService
from app.labour.domain.contraction.services.start_contraction import StartContractionService
from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.exceptions import LabourHasNoActiveContraction
from app.labour.domain.labour.services.begin_labour import BeginLabourService


def test_can_end_contraction(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(sample_labour)
    EndContractionService().end_contraction(sample_labour, intensity=CONTRACTION_MAX_INTENSITY)


def test_cannot_end_contraction_that_doesnt_exist(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    with pytest.raises(LabourHasNoActiveContraction):
        EndContractionService().end_contraction(sample_labour, intensity=CONTRACTION_MAX_INTENSITY)
