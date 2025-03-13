from pydantic import BaseModel


class SendSubscriberInviteRequest(BaseModel):
    invite_email: str
