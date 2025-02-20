from pydantic import BaseModel

from app.application.dtos.subscriber import SubscriberDTO
from app.application.dtos.subscription import SubscriptionDTO


class SubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]


class LabourSubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]
    subscribers: list[SubscriberDTO]


class SubscriptionResponse(BaseModel):
    subscription: SubscriptionDTO
