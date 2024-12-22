from pydantic import BaseModel

from app.application.dtos.birthing_person import BirthingPersonDTO


class BirthingPersonResponse(BaseModel):
    birthing_person: BirthingPersonDTO
