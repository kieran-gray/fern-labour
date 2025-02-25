from datetime import datetime

from pydantic import BaseModel

from app.domain.labour_update.enums import LabourUpdateType


class LabourUpdateRequest(BaseModel):
    labour_update_type: LabourUpdateType
    message: str
    sent_time: datetime | None = None
