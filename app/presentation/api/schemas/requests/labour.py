from datetime import datetime

from pydantic import BaseModel


class BeginLabourRequest(BaseModel):
    first_labour: bool | None = None


class CompleteLabourRequest(BaseModel):
    end_time: datetime | None = None
    notes: str | None = None
