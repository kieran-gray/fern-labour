from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, status

from src.admin.application.services.contact_service import ContactService
from src.admin.presentation.api.schemas.requests.contact import ContactUsRequest
from src.api.exception_handler import ExceptionSchema
from src.core.infrastructure.security.interfaces.request_verification_service import (
    RequestVerificationService,
)
from src.setup.ioc.di_component_enum import ComponentEnum

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
    request: Request,
    request_data: ContactUsRequest,
    request_verification_service: Annotated[
        RequestVerificationService, FromComponent(ComponentEnum.DEFAULT)
    ],
    contact_service: Annotated[ContactService, FromComponent(ComponentEnum.ADMIN)],
) -> None:
    await request_verification_service.verify(token=request_data.token, ip=request.client.host)  # type: ignore
    await contact_service.send_contact_email(
        email=request_data.email,
        name=request_data.name,
        message=request_data.message,
        user_id=request_data.user_id,
    )
    return None
