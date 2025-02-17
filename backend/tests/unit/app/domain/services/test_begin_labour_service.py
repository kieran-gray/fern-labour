import pytest

from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.exceptions import LabourAlreadyBegun
from app.domain.services.begin_labour import BeginLabourService


def test_can_begin_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    assert sample_labour.current_phase is LabourPhase.EARLY


def test_cannot_begin_labour_already_begun(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    with pytest.raises(LabourAlreadyBegun):
        BeginLabourService().begin_labour(sample_labour)
