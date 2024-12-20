from pydantic import BaseModel

from app.application.dtos.contact import ContactDTO


class RegisterBirthingPersonRequest(BaseModel):
    name: str
    first_labor: bool


class AddContactRequest(BaseModel):
    contact: ContactDTO
