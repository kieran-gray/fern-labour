from pydantic import BaseModel

from app.application.dtos.subscription import SubscriptionDTO
from app.application.dtos.user_summary import UserSummaryDTO
from app.labour.application.dtos.labour import LabourDTO


class SubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]


class SubscriberSubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]
    birthing_persons: list[UserSummaryDTO]


# TODO This is getting messy
class SubscriptionDataResponse(BaseModel):
    subscription: SubscriptionDTO
    birthing_person: UserSummaryDTO
    labour: LabourDTO


class LabourSubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]
    subscribers: list[UserSummaryDTO]


class SubscriptionResponse(BaseModel):
    subscription: SubscriptionDTO
