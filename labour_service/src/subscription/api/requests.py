from pydantic import BaseModel


class RemoveSubscriberRequest(BaseModel):
    subscription_id: str


class BlockSubscriberRequest(BaseModel):
    subscription_id: str


class UpdateRoleRequest(BaseModel):
    subscription_id: str
    role: str


class UpdateContactMethodsRequest(BaseModel):
    subscription_id: str
    contact_methods: list[str]


class SubscribeToRequest(BaseModel):
    token: str


class UnsubscribeFromRequest(BaseModel):
    labour_id: str


class SendSubscriberInviteRequest(BaseModel):
    invite_email: str
