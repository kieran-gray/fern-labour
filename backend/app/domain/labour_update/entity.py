from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from app.domain.labour_update.vo_labour_update_id import LabourUpdateId
from app.domain.base.entity import Entity
from app.domain.labour.vo_labour_id import LabourId
from app.domain.labour_update.enums import LabourUpdateType


@dataclass(eq=False, kw_only=True)
class LabourUpdate(Entity[LabourUpdateId]):
    labour_id: LabourId
    message: str
    labour_update_type: LabourUpdateType
    sent_time: datetime

    @classmethod
    def create(
        cls,
        *,
        labour_update_type: LabourUpdateType,
        labour_id: LabourId,
        message: str,
        sent_time: datetime | None = None,
        labour_update_id: UUID | None = None,
    ) -> Self:
        sent_time = sent_time or datetime.now(UTC)
        labour_update_id = labour_update_id or uuid4()
        return cls(
            id_=LabourUpdateId(labour_update_id),
            labour_update_type=labour_update_type,
            labour_id=labour_id,
            message=message,
            sent_time=sent_time,
        )
