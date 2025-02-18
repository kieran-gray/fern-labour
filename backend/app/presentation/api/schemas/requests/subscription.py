from pydantic import BaseModel


class RemoveSubscriberRequest(BaseModel):
    subscription_id: str


class UpdateRoleRequest(BaseModel):
    subscription_id: str
    role: str


class UpdateContactMethodsRequest(BaseModel):
    subscription_id: str
    contact_methods: list[str]
