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


class UpdateContractionRequest(BaseModel):
    contraction_id: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    intensity: int | None = None
    notes: str | None = None
