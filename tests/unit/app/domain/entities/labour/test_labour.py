from datetime import datetime
from uuid import UUID

from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.entity import Labour
from app.domain.labour.vo_labour_id import LabourId


def test_labour_init():
    labour_id = UUID("12345678-1234-5678-1234-567812345678")
    birthing_person_id = BirthingPersonId("87654321-4321-1234-8765-567812345678")
    start_time: datetime = datetime.now()

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
