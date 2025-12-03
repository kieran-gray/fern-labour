from datetime import datetime
from uuid import uuid4

import pytest

from src.labour.domain.contraction.constants import CONTRACTION_MAX_INTENSITY
from src.labour.domain.contraction.exceptions import (
    CannotDeleteActiveContraction,
    ContractionNotFoundById,
)
from src.labour.domain.contraction.services.delete_contraction import DeleteContractionService
from src.labour.domain.contraction.services.end_contraction import EndContractionService
from src.labour.domain.contraction.services.start_contraction import StartContractionService
from src.labour.domain.contraction.value_objects.contraction_id import ContractionId
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.exceptions import LabourAlreadyCompleted
from src.labour.domain.labour.services.begin_labour import BeginLabourService
from src.labour.domain.labour.services.complete_labour import CompleteLabourService


def test_can_delete_contraction(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=datetime(2020, 1, 1, 1, 0),
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=datetime(2020, 1, 1, 1, 1),
    )
    assert len(labour.contractions) == 1
    DeleteContractionService().delete_contraction(
        labour=sample_labour, contraction_id=labour.contractions[0].id_
    )
    assert len(labour.contractions) == 0


def test_cannot_delete_contraction_that_doesnt_exist(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    with pytest.raises(ContractionNotFoundById):
        DeleteContractionService().delete_contraction(
            sample_labour, contraction_id=ContractionId(uuid4())
        )


def test_cannot_delete_active_contraction(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    labour = StartContractionService().start_contraction(labour=sample_labour)
    with pytest.raises(CannotDeleteActiveContraction):
        DeleteContractionService().delete_contraction(
            sample_labour, contraction_id=labour.contractions[0].id_
        )


def test_cannot_delete_contraction_in_completed_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(sample_labour)
    EndContractionService().end_contraction(sample_labour, intensity=CONTRACTION_MAX_INTENSITY)
    labour = CompleteLabourService().complete_labour(sample_labour)

    with pytest.raises(LabourAlreadyCompleted):
        DeleteContractionService().delete_contraction(
            sample_labour, contraction_id=labour.contractions[0].id_
        )
