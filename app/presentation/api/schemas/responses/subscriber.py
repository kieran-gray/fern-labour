from pydantic import BaseModel

from app.application.dtos.subscriber import SubscriberDTO


class SubscriberResponse(BaseModel):
    subscriber: SubscriberDTO
