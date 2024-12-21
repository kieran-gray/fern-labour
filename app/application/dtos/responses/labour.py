from pydantic import BaseModel

from app.application.dtos.labour import LabourDTO
from app.application.dtos.labour_summary import LabourSummaryDTO


class BeginLabourResponse(BaseModel):
    labour: LabourDTO


class CompleteLabourResponse(BaseModel):
    labour: LabourDTO


class StartContractionResponse(BaseModel):
    labour: LabourDTO


class EndContractionResponse(BaseModel):
    labour: LabourDTO


class GetActiveLabourResponse(BaseModel):
    labour: LabourDTO


class GetActiveLabourSummaryResponse(BaseModel):
    labour: LabourSummaryDTO
