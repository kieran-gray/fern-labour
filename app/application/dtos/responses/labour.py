from pydantic import BaseModel

from app.application.dtos.labour import LabourDTO


class BeginLabourResponse(BaseModel):
    labour: LabourDTO


class CompleteLabourResponse(BaseModel):
    labour: LabourDTO


class StartContractionResponse(BaseModel):
    labour: LabourDTO


class EndContractionResponse(BaseModel):
    labour: LabourDTO
