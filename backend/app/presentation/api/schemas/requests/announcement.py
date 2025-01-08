from datetime import datetime

from pydantic import BaseModel


class MakeAnnouncementRequest(BaseModel):
    message: str
    sent_time: datetime | None = None
