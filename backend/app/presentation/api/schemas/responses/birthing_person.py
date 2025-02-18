from pydantic import BaseModel

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.application.dtos.birthing_person_summary import BirthingPersonSummaryDTO


class BirthingPersonResponse(BaseModel):
    birthing_person: BirthingPersonDTO


class BirthingPersonSummaryResponse(BaseModel):
    birthing_person: BirthingPersonSummaryDTO
