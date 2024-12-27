from pydantic import BaseModel


class RegisterSubscriberRequest(BaseModel):
    contact_methods: list[str]


class SubscribeToRequest(BaseModel):
    token: str
