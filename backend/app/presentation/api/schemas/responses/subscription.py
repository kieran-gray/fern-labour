from pydantic import BaseModel

from app.application.dtos.subscription import SubscriptionDTO


class SubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]


class SubscriptionResponse(BaseModel):
    subscription: SubscriptionDTO
