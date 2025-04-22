from datetime import datetime
from uuid import uuid4

import pytest

from src.labour.domain.contraction.constants import CONTRACTION_MAX_INTENSITY
from src.labour.domain.contraction.exceptions import (
    CannotUpdateActiveContraction,
    ContractionIntensityInvalid,
    ContractionNotFoundById,
    ContractionsOverlappingAfterUpdate,
    ContractionStartTimeAfterEndTime,
)
from src.labour.domain.contraction.services.end_contraction import EndContractionService
from src.labour.domain.contraction.services.start_contraction import StartContractionService
from src.labour.domain.contraction.services.update_contraction import UpdateContractionService
from src.labour.domain.contraction.value_objects.contraction_id import ContractionId
from src.labour.domain.labour.entity import Labour
from src.labour.domain.labour.exceptions import LabourAlreadyCompleted
from src.labour.domain.labour.services.begin_labour import BeginLabourService
from src.labour.domain.labour.services.complete_labour import CompleteLabourService


def test_can_update_contraction_notes(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_start_time = datetime(2020, 1, 1, 1, 0)
    contraction_end_time = datetime(2020, 1, 1, 1, 1)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_end_time,
    )
    assert labour.contractions[0].notes is None
    UpdateContractionService().update_contraction(
        labour=sample_labour, contraction_id=labour.contractions[0].id_, notes="Hello test"
    )
    assert labour.contractions[0].notes == "Hello test"


def test_can_update_contraction_intensity(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_start_time = datetime(2020, 1, 1, 1, 0)
    contraction_end_time = datetime(2020, 1, 1, 1, 1)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_end_time,
    )
    UpdateContractionService().update_contraction(
        labour=sample_labour, contraction_id=labour.contractions[0].id_, intensity=2
    )
    assert labour.contractions[0].intensity == 2


def test_cannot_update_contraction_intensity_invalid(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_start_time = datetime(2020, 1, 1, 1, 0)
    contraction_end_time = datetime(2020, 1, 1, 1, 1)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_end_time,
    )
    with pytest.raises(ContractionIntensityInvalid):
        UpdateContractionService().update_contraction(
            labour=sample_labour,
            contraction_id=labour.contractions[0].id_,
            intensity=CONTRACTION_MAX_INTENSITY + 10,
        )


def test_can_update_contraction_start_time(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_start_time = datetime(2020, 1, 1, 1, 0)
    contraction_end_time = datetime(2020, 1, 1, 1, 1)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_end_time,
    )
    assert labour.contractions[0].duration.duration_seconds == 60
    UpdateContractionService().update_contraction(
        labour=sample_labour,
        contraction_id=labour.contractions[0].id_,
        start_time=datetime(2020, 1, 1, 1, 0, 30),
    )
    assert labour.contractions[0].duration.duration_seconds == 30


def test_can_update_contraction_start_time_and_end_time(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_start_time = datetime(2020, 1, 1, 1, 0)
    contraction_end_time = datetime(2020, 1, 1, 1, 1)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_end_time,
    )
    assert labour.contractions[0].duration.duration_seconds == 60
    UpdateContractionService().update_contraction(
        labour=sample_labour,
        contraction_id=labour.contractions[0].id_,
        start_time=datetime(2020, 1, 1, 2, 0),
        end_time=datetime(2020, 1, 1, 2, 1),
    )
    assert labour.contractions[0].duration.duration_seconds == 60


def test_can_update_contraction_end_time(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_start_time = datetime(2020, 1, 1, 1, 0)
    contraction_end_time = datetime(2020, 1, 1, 1, 1)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_end_time,
    )
    assert labour.contractions[0].duration.duration_seconds == 60
    UpdateContractionService().update_contraction(
        labour=sample_labour,
        contraction_id=labour.contractions[0].id_,
        end_time=datetime(2020, 1, 1, 1, 0, 30),
    )
    assert labour.contractions[0].duration.duration_seconds == 30


def test_cannot_update_contraction_end_time_before_start_time(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_start_time = datetime(2020, 1, 1, 1, 1)
    contraction_end_time = datetime(2020, 1, 1, 1, 2)
    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_end_time,
    )
    with pytest.raises(ContractionStartTimeAfterEndTime):
        UpdateContractionService().update_contraction(
            labour=sample_labour,
            contraction_id=labour.contractions[0].id_,
            end_time=datetime(2020, 1, 1, 1, 0),
        )


def test_cannot_update_contraction_end_time_before_start_time_1(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_1_start_time = datetime(2020, 1, 1, 1, 1)
    contraction_1_end_time = datetime(2020, 1, 1, 1, 2)
    contraction_2_start_time = datetime(2020, 1, 1, 1, 3)
    contraction_2_end_time = datetime(2020, 1, 1, 1, 4)

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_1_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_1_end_time,
    )

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_2_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_2_end_time,
    )

    with pytest.raises(ContractionsOverlappingAfterUpdate):
        UpdateContractionService().update_contraction(
            labour=sample_labour,
            contraction_id=labour.contractions[0].id_,
            end_time=datetime(2020, 1, 1, 1, 3, 1),
        )


def test_cannot_update_contraction_end_time_before_start_time_2(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_1_start_time = datetime(2020, 1, 1, 1, 1)
    contraction_1_end_time = datetime(2020, 1, 1, 1, 2)
    contraction_2_start_time = datetime(2020, 1, 1, 1, 3)
    contraction_2_end_time = datetime(2020, 1, 1, 1, 4)

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_1_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_1_end_time,
    )

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_2_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_2_end_time,
    )

    with pytest.raises(ContractionsOverlappingAfterUpdate):
        UpdateContractionService().update_contraction(
            labour=sample_labour,
            contraction_id=labour.contractions[0].id_,
            end_time=datetime(2020, 1, 1, 1, 5),
        )


def test_cannot_update_contraction_end_time_before_start_time_3(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_1_start_time = datetime(2020, 1, 1, 1, 1)
    contraction_1_end_time = datetime(2020, 1, 1, 1, 2)
    contraction_2_start_time = datetime(2020, 1, 1, 1, 3)
    contraction_2_end_time = datetime(2020, 1, 1, 1, 4)

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_1_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_1_end_time,
    )

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_2_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_2_end_time,
    )

    with pytest.raises(ContractionsOverlappingAfterUpdate):
        UpdateContractionService().update_contraction(
            labour=sample_labour,
            contraction_id=labour.contractions[1].id_,
            start_time=datetime(2020, 1, 1, 1, 1, 59),
        )


def test_can_update_contraction_start_time_to_previous_end_time(sample_labour: Labour):
    labour = BeginLabourService().begin_labour(sample_labour)
    contraction_1_start_time = datetime(2020, 1, 1, 1, 1)
    contraction_1_end_time = datetime(2020, 1, 1, 1, 2)
    contraction_2_start_time = datetime(2020, 1, 1, 1, 3)
    contraction_2_end_time = datetime(2020, 1, 1, 1, 4)

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_1_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_1_end_time,
    )

    StartContractionService().start_contraction(
        labour=sample_labour,
        start_time=contraction_2_start_time,
    )
    EndContractionService().end_contraction(
        labour=sample_labour,
        intensity=CONTRACTION_MAX_INTENSITY,
        end_time=contraction_2_end_time,
    )

    UpdateContractionService().update_contraction(
        labour=sample_labour,
        contraction_id=labour.contractions[1].id_,
        start_time=datetime(2020, 1, 1, 1, 2),
    )


def test_cannot_update_contraction_that_doesnt_exist(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    with pytest.raises(ContractionNotFoundById):
        UpdateContractionService().update_contraction(
            sample_labour, contraction_id=ContractionId(uuid4())
        )


def test_cannot_update_active_contraction(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    labour = StartContractionService().start_contraction(labour=sample_labour)
    with pytest.raises(CannotUpdateActiveContraction):
        UpdateContractionService().update_contraction(
            sample_labour, contraction_id=labour.contractions[0].id_
        )


def test_cannot_update_contraction_in_completed_labour(sample_labour: Labour):
    BeginLabourService().begin_labour(sample_labour)
    StartContractionService().start_contraction(sample_labour)
    EndContractionService().end_contraction(sample_labour, intensity=CONTRACTION_MAX_INTENSITY)
    labour = CompleteLabourService().complete_labour(sample_labour)

    with pytest.raises(LabourAlreadyCompleted):
        UpdateContractionService().update_contraction(
            sample_labour, contraction_id=labour.contractions[0].id_
        )
