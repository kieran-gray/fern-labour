from datetime import datetime

from pydantic import BaseModel


class StartContractionRequest(BaseModel):
    intensity: int | None = None
    start_time: datetime | None = None
    notes: str | None = None


class EndContractionRequest(BaseModel):
    intensity: int
    end_time: datetime | None = None
    notes: str | None = None
