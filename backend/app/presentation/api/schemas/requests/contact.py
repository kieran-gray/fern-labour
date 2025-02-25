from pydantic import BaseModel


class ContactUsRequest(BaseModel):
    email: str
    name: str
    message: str
    token: str
    user_id: str | None = None
