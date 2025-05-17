from datetime import datetime

from pydantic import BaseModel

from src.labour.domain.labour_update.enums import LabourUpdateType


class LabourUpdateRequest(BaseModel):
    labour_update_type: LabourUpdateType
    message: str
    sent_time: datetime | None = None


class UpdateLabourUpdateRequest(BaseModel):
    labour_update_id: str
    labour_update_type: LabourUpdateType | None = None
    message: str | None = None


class DeleteLabourUpdateRequest(BaseModel):
    labour_update_id: str
