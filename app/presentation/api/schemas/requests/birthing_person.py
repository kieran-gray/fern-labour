from pydantic import BaseModel


class RegisterBirthingPersonRequest(BaseModel):
    first_labor: bool


class AddSubscriberRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: str | None
    email: str | None
    contact_methods: list[str]
