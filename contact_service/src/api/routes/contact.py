from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, status

from src.api.exception_handler import ExceptionSchema
from src.api.requests import ContactUsRequest
from src.application.contact_message_service import ContactMessageService
from src.infrastructure.security.request_verification.interface import (
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
    contact_service: Annotated[ContactMessageService, FromComponent(ComponentEnum.DEFAULT)],
) -> None:
    await request_verification_service.verify(token=request_data.token, ip=request.client.host)  # type: ignore
    await contact_service.send_contact_email(
        email=request_data.email,
        name=request_data.name,
        message=request_data.message,
        user_id=request_data.user_id,
    )
    return


@contact_us_router.post(
    "/store",
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_201_CREATED,
)
@inject
async def contact_us_store(
    request: Request,
    request_data: ContactUsRequest,
    request_verification_service: Annotated[
        RequestVerificationService, FromComponent(ComponentEnum.DEFAULT)
    ],
    contact_service: Annotated[ContactMessageService, FromComponent(ComponentEnum.DEFAULT)],
) -> None:
    await request_verification_service.verify(token=request_data.token, ip=request.client.host)  # type: ignore
    await contact_service.create_message(
        category=request_data.category,
        email=request_data.email,
        name=request_data.name,
        message=request_data.message,
        data=request_data.data,
        user_id=request_data.user_id,
    )
    return
