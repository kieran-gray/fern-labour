from pydantic import BaseModel

from app.application.dtos.birthing_person_summary import BirthingPersonSummaryDTO
from app.application.dtos.labour import LabourDTO
from app.application.dtos.subscriber import SubscriberDTO
from app.application.dtos.subscription import SubscriptionDTO


class SubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]


class SubscriberSubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]
    birthing_persons: list[BirthingPersonSummaryDTO]


# TODO This is getting messy
class SubscriptionDataResponse(BaseModel):
    subscription: SubscriptionDTO
    birthing_person: BirthingPersonSummaryDTO
    labour: LabourDTO


class LabourSubscriptionsResponse(BaseModel):
    subscriptions: list[SubscriptionDTO]
    subscribers: list[SubscriberDTO]


class SubscriptionResponse(BaseModel):
    subscription: SubscriptionDTO
