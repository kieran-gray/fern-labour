from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form, Request, status

from src.api.exception_handler import ExceptionSchema
from src.notification.application.services.notification_service import NotificationService
from src.notification.infrastructure.security.request_verification_service import (
    RequestVerificationService,
)
from src.notification.infrastructure.twilio.status_mapping import TWILIO_STATUS_MAPPING
from src.setup.ioc.di_component_enum import ComponentEnum

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
    request: Request,
    notification_service: Annotated[
        NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
    ],
    request_verification_service: Annotated[
        RequestVerificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
    ],
    MessageSid: str | None = Form(None),
    MessageStatus: str | None = Form(None),
) -> None:
    form_data = await request.form()
    # Traefik seems to redirect from https -> http, which causes the request verification
    # to fail as twilio expects (and does use) the https url.
    request_url = str(request.url).replace("http://", "https://")
    request_verification_service.verify(
        uri=request_url,
        params=form_data,
        signature=request.headers.get("X-Twilio-Signature", ""),
    )
    if not MessageSid or not MessageStatus:
        return
    if status := TWILIO_STATUS_MAPPING.get(MessageStatus):
        await notification_service.status_callback(external_id=MessageSid, status=status)
