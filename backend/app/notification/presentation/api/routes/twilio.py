from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form, status

from app.api.exception_handler import ExceptionSchema
from app.notification.application.services.notification_service import NotificationService
from app.notification.infrastructure.twilio.status_mapping import TWILIO_STATUS_MAPPING
from app.setup.ioc.di_component_enum import ComponentEnum

twilio_router = APIRouter(prefix="/twilio", tags=["Twilio"])


@twilio_router.post(
    "/message-status",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def twilio_webhook(
    notification_service: Annotated[
        NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
    ],
    MessageSid: str | None = Form(None),
    MessageStatus: str | None = Form(None),
) -> None:
    if not MessageSid or not MessageStatus:
        return
    if status := TWILIO_STATUS_MAPPING.get(MessageStatus):
        await notification_service.status_callback(external_id=MessageSid, status=status)
