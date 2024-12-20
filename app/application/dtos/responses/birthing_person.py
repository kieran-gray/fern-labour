from pydantic import BaseModel

from app.application.dtos.birthing_person import BirthingPersonDTO


class RegisterBirthingPersonResponse(BaseModel):
    birthing_person: BirthingPersonDTO


class AddContactResponse(BaseModel):
    birthing_person: BirthingPersonDTO
