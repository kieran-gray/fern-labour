from pydantic import BaseModel


class AddSubscriberRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: str | None
    email: str | None
    contact_methods: list[str]
