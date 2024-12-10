from pydantic import BaseModel

from app.application.dtos.labor_session_dto import ContractionDTO, LaborSessionDTO


class StartLaborSessionResponse(BaseModel):
    labor_session: LaborSessionDTO


class CompleteLaborSessionResponse(BaseModel):
    labor_session: LaborSessionDTO


class StartContractionResponse(BaseModel):
    contraction: ContractionDTO


class EndContractionResponse(BaseModel):
    contraction: ContractionDTO
