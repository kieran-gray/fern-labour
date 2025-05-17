from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from fern_labour_core.entity import Entity

from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.labour.domain.labour_update.enums import LabourUpdateType
from src.labour.domain.labour_update.value_objects.labour_update_id import LabourUpdateId


@dataclass(eq=False, kw_only=True)
class LabourUpdate(Entity[LabourUpdateId]):
    labour_id: LabourId
    message: str
    labour_update_type: LabourUpdateType
    sent_time: datetime
    edited: bool

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
            edited=False,
        )

    def update(
        self, message: str | None = None, labour_update_type: LabourUpdateType | None = None
    ) -> None:
        if message is not None:
            self.message = message
            self.edited = True
        if labour_update_type:
            self.labour_update_type = labour_update_type
