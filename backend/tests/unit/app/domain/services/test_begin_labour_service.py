import pytest

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.exceptions import BirthingPersonHasActiveLabour
from app.domain.services.begin_labour import BeginLabourService


def test_can_begin_labour(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)


def test_cannot_begin_labour_with_active_labour(sample_birthing_person: BirthingPerson):
    BeginLabourService().begin_labour(sample_birthing_person, True)
    with pytest.raises(BirthingPersonHasActiveLabour):
        BeginLabourService().begin_labour(sample_birthing_person, True)
