from pydantic import BaseModel


class CheckoutResponse(BaseModel):
    id: str
    url: str | None
