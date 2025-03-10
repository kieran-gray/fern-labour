from pydantic import BaseModel


class CreateCheckoutRequest(BaseModel):
    upgrade: str
    labour_id: str
    success_url: str
    cancel_url: str
