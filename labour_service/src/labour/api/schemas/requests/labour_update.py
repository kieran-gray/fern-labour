from datetime import datetime

from pydantic import BaseModel, Field

from src.labour.domain.labour_update.enums import LabourUpdateType

LABOUR_UPDATE_MAX_LENGTH = 1000


class LabourUpdateRequest(BaseModel):
    labour_update_type: LabourUpdateType
    message: str = Field(max_length=LABOUR_UPDATE_MAX_LENGTH)
    sent_time: datetime | None = None


class UpdateLabourUpdateRequest(BaseModel):
    labour_update_id: str
    labour_update_type: LabourUpdateType | None = None
    message: str | None = Field(default=None, max_length=LABOUR_UPDATE_MAX_LENGTH)


class DeleteLabourUpdateRequest(BaseModel):
    labour_update_id: str
