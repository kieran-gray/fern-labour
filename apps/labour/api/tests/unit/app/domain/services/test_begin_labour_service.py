import pytest

from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.enums import LabourPhase
from src.labour.domain.labour.exceptions import LabourAlreadyBegun
from src.labour.domain.labour.services.begin_labour import BeginLabourService


def test_can_begin_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    assert sample_labour.current_phase is LabourPhase.EARLY


def test_cannot_begin_labour_already_begun(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    with pytest.raises(LabourAlreadyBegun):
        BeginLabourService().begin_labour(sample_labour)
