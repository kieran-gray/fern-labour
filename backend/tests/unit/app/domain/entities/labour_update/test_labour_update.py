from datetime import UTC, datetime
from uuid import UUID

from app.domain.labour_update.entity import LabourUpdate
from app.domain.labour_update.vo_labour_update_id import LabourUpdateId
from app.domain.labour_update.enums import LabourUpdateType
from app.domain.labour.vo_labour_id import LabourId


def test_labour_update_init():
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))
    labour_update_id: UUID = UUID("87654321-1234-5678-1234-567812345678")
    sent_time: datetime = datetime.now(UTC)
    message: str = "Test Message"

    vo_labour_update_id = LabourUpdateId(labour_update_id)

    direct_labour_update = LabourUpdate(
        id_=vo_labour_update_id,
        labour_update_type=LabourUpdateType.ANNOUNCEMENT,
        labour_id=labour_id,
        message=message,
        sent_time=sent_time,
    )

    indirect_labour_update = LabourUpdate.create(
        labour_update_type=LabourUpdateType.ANNOUNCEMENT,
        labour_update_id=labour_update_id,
        labour_id=labour_id,
        message=message,
        sent_time=sent_time
    )

    assert isinstance(indirect_labour_update, LabourUpdate)
    assert direct_labour_update.id_ == vo_labour_update_id == indirect_labour_update.id_
    assert direct_labour_update == indirect_labour_update


def test_labour_update_init_default_values():
    labour_id = LabourId(UUID("12345678-1234-5678-1234-567812345678"))
    message: str = "Test user"

    labour_update = LabourUpdate.create(
        labour_update_type=LabourUpdateType.STATUS_UPDATE, labour_id=labour_id, message=message
    )
    assert isinstance(labour_update, LabourUpdate)
    assert labour_update.sent_time is not None
    assert labour_update.id_ is not None
