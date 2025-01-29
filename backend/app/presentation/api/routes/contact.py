from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from app.application.events.producer import EventProducer
from app.domain.base.event import DomainEvent
from app.presentation.api.schemas.requests.contact import ContactUsRequest
from app.presentation.exception_handler import ExceptionSchema
from app.setup.ioc.di_component_enum import ComponentEnum

contact_us_router = APIRouter(prefix="/contact-us", tags=["Contact Us"])


@contact_us_router.post(
    "/",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def contact_us_send_message(
    request_data: ContactUsRequest,
    event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
) -> None:
    event = DomainEvent.create(data=request_data.model_dump(), event_type="contact-us.message-sent")
    await event_producer.publish(event=event)
    return None
