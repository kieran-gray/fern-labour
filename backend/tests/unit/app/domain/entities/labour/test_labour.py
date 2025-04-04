from datetime import UTC, datetime
from uuid import UUID

from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.user.domain.value_objects.user_id import UserId


def test_labour_init():
    labour_id = UUID("12345678-1234-5678-1234-567812345678")
    birthing_person_id = UserId("87654321-4321-1234-8765-567812345678")
    due_date: datetime = datetime.now(UTC)

    vo_labour_id = LabourId(labour_id)

    direct_labour = Labour(
        id_=vo_labour_id,
        birthing_person_id=birthing_person_id,
        due_date=due_date,
        first_labour=True,
    )

    indirect_labour = Labour.plan(
        labour_id=labour_id,
        birthing_person_id=birthing_person_id,
        due_date=due_date,
        first_labour=True,
    )

    assert isinstance(indirect_labour, Labour)
    assert direct_labour.id_ == vo_labour_id == indirect_labour.id_
    assert direct_labour == indirect_labour
