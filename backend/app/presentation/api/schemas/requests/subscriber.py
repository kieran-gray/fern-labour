from pydantic import BaseModel


class SubscribeToRequest(BaseModel):
    token: str


class UnsubscribeFromRequest(BaseModel):
    labour_id: str
