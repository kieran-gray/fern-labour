from typing import Any

from pydantic import BaseModel


class ContactUsRequest(BaseModel):
    category: str
    email: str
    name: str
    message: str
    token: str
    data: dict[str, Any] | None = None
    user_id: str | None = None
