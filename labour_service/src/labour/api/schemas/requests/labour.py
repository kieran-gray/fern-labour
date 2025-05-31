from datetime import datetime

from pydantic import BaseModel, Field

LABOUR_NAME_MAX_LENGTH = 255


class PlanLabourRequest(BaseModel):
    first_labour: bool
    due_date: datetime
    labour_name: str | None = Field(default=None, max_length=LABOUR_NAME_MAX_LENGTH)


class CompleteLabourRequest(BaseModel):
    end_time: datetime | None = None
    notes: str | None = None


class SendInviteRequest(BaseModel):
    invite_email: str
    labour_id: str
