from pydantic import BaseModel


class RemoveSubscriberRequest(BaseModel):
    subscriber_id: str


class SendInviteRequest(BaseModel):
    invite_email: str
