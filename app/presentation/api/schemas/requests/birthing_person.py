from pydantic import BaseModel


class RegisterBirthingPersonRequest(BaseModel):
    name: str
    first_labor: bool


class AddContactRequest(BaseModel):
    name: str
    phone_number: str | None
    email: str | None
    contact_methods: list[str]
