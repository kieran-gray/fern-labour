from pydantic import BaseModel

from src.labour.application.dtos.labour import LabourDTO
from src.subscription.application.dtos.subscription import SubscriptionDTO
from src.user.application.dtos.user_summary import UserSummaryDTO


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
