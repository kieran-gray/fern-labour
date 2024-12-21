import pytest

from app.domain.birthing_person.entity import BirthingPerson

from app.domain.labour.exceptions import LabourHasNoActiveContraction
from app.domain.contraction.constants import CONTRACTION_MAX_INTENSITY
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour

from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.start_contraction import StartContractionService
from app.domain.services.end_contraction import EndContractionService


def test_can_end_contraction(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person)
    StartContractionService().start_contraction(sample_birthing_person)
    EndContractionService().end_contraction(sample_birthing_person, intensity=CONTRACTION_MAX_INTENSITY)


def test_cannot_end_contraction_without_active_labour(sample_birthing_person: BirthingPerson):
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        EndContractionService().end_contraction(sample_birthing_person, intensity=CONTRACTION_MAX_INTENSITY)


def test_cannot_end_contraction_that_doesnt_exist(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person)
    with pytest.raises(LabourHasNoActiveContraction):
        EndContractionService().end_contraction(sample_birthing_person, intensity=CONTRACTION_MAX_INTENSITY)
