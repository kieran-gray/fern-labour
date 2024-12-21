import pytest

from app.domain.birthing_person.entity import BirthingPerson

from app.domain.labour.exceptions import CannotCompleteLabourWithActiveContraction

from app.domain.birthing_person.exceptions import BirthingPersonDoesNotHaveActiveLabour
from app.domain.services.complete_labour import CompleteLabourService
from app.domain.services.begin_labour import BeginLabourService
from app.domain.services.start_contraction import StartContractionService


def test_can_complete_labour(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person)
    CompleteLabourService().complete_labour(sample_birthing_person)


def test_cannot_complete_labour_that_doesnt_exist(sample_birthing_person: BirthingPerson):
    with pytest.raises(BirthingPersonDoesNotHaveActiveLabour):
        CompleteLabourService().complete_labour(sample_birthing_person)


def test_cannot_complete_labour_with_active_contraction(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person)
    StartContractionService().start_contraction(sample_birthing_person, intensity=1)

    with pytest.raises(CannotCompleteLabourWithActiveContraction):
        CompleteLabourService().complete_labour(sample_birthing_person)
