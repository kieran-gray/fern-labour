from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import pytest

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.contraction.entity import Contraction
from app.domain.labour.entity import Labour
from app.domain.labour.enums import LabourPhase
from app.domain.labour.vo_labour_id import LabourId


def generate_contractions(length: float, intensity: int) -> dict[str, Any]:
    # TODO the fact that I need to do this in here indicates that the phase update should
    # be a domain service.

    contraction_list = []
    last_start_time = None
    for _ in range(5):
        start_time = last_start_time or datetime.now(UTC)
        end_time = start_time + timedelta(minutes=length)

        contraction = Contraction.start(labour_id=LabourId(uuid4()), start_time=start_time)
        contraction.end(end_time=end_time, intensity=intensity)

        contraction_list.append(contraction)
        last_start_time = start_time

    return contraction_list


def test_labour_init():
    labour_id = UUID("12345678-1234-5678-1234-567812345678")
    birthing_person_id = BirthingPersonId("87654321-4321-1234-8765-567812345678")
    start_time: datetime = datetime.now(UTC)

    vo_labour_id = LabourId(labour_id)

    direct_labour = Labour(
        id_=vo_labour_id,
        birthing_person_id=birthing_person_id,
        start_time=start_time,
        first_labour=True,
    )

    indirect_labour = Labour.begin(
        labour_id=labour_id,
        birthing_person_id=birthing_person_id,
        start_time=start_time,
        first_labour=True,
    )

    assert isinstance(indirect_labour, Labour)
    assert direct_labour.id_ == vo_labour_id == indirect_labour.id_
    assert direct_labour == indirect_labour


@pytest.mark.parametrize(
    "contraction_length,contraction_intensity,expected_labour_phase",
    [
        (0.5, 6, LabourPhase.EARLY),
        (0.99, 6, LabourPhase.EARLY),
        (1, 6, LabourPhase.ACTIVE),
        (1.49, 8, LabourPhase.ACTIVE),
        (1.5, 8, LabourPhase.TRANSITION),
    ],
)
def test_labour_phase_update(
    contraction_length: float, contraction_intensity: int, expected_labour_phase: LabourPhase
):
    labour = Labour.begin(
        labour_id=uuid4(),
        birthing_person_id=BirthingPersonId("87654321-4321-1234-8765-567812345678"),
        start_time=datetime.now(UTC),
        first_labour=True,
    )
    labour.contractions = generate_contractions(
        length=contraction_length, intensity=contraction_intensity
    )
    assert labour.current_phase is LabourPhase.EARLY
    labour._update_labour_phase()
    assert labour.current_phase is expected_labour_phase
