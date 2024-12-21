import pytest

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import LabourCompleted, LabourHasActiveContraction
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.start_contraction import StartContractionService


def test_can_start_contraction(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person)
    StartContractionService().start_contraction(sample_birthing_person)


def test_cannot_start_multiple_contractions(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person)
    StartContractionService().start_contraction(sample_birthing_person)
    with pytest.raises(LabourHasActiveContraction):
        StartContractionService().start_contraction(sample_birthing_person)


def test_cannot_start_contraction_without_active_labour(sample_birthing_person: BirthingPerson):
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        StartContractionService().start_contraction(sample_birthing_person)


def test_cannot_start_contraction_for_completed_labour(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person)
    sample_birthing_person.active_labour.current_phase = LabourPhase.COMPLETE
    with pytest.raises(LabourCompleted):
        StartContractionService().start_contraction(sample_birthing_person)
