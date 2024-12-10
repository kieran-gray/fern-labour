from uuid import UUID

from pydantic import BaseModel


class StartLaborSessionRequest(BaseModel):
    user_id: UUID
    first_labor: bool


class CompleteLaborSessionRequest(BaseModel):
    session_id: UUID
    notes: str | None = None


class StartContractionRequest(BaseModel):
    session_id: UUID
    intensity: int
    notes: str | None = None


class EndContractionRequest(BaseModel):
    session_id: UUID
