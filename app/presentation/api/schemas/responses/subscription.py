from pydantic import BaseModel

from app.application.dtos.birthing_person_summary import BirthingPersonSummaryDTO


class GetSubscriptionsResponse(BaseModel):
    subscriptions: list[BirthingPersonSummaryDTO]
