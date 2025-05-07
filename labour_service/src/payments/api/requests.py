from pydantic import BaseModel


class CreateCheckoutRequest(BaseModel):
    upgrade: str
    subscription_id: str
    success_url: str
    cancel_url: str
