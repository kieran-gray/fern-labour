import pytest

from app.domain.labour.entity import Labour
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.contraction.constants import CONTRACTION_MAX_INTENSITY
from app.domain.labour.exceptions import LabourHasNoActiveContraction
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.end_contraction import EndContractionService
from app.domain.services.start_contraction import StartContractionService


def test_can_end_contraction(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(sample_labour)
    EndContractionService().end_contraction(
        sample_labour, intensity=CONTRACTION_MAX_INTENSITY
    )


def test_cannot_end_contraction_that_doesnt_exist(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    with pytest.raises(LabourHasNoActiveContraction):
        EndContractionService().end_contraction(
            sample_labour, intensity=CONTRACTION_MAX_INTENSITY
        )
