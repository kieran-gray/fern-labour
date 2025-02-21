from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from app.application.services.birthing_person_service import BirthingPersonService
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.infrastructure.auth.interfaces.controller import AuthController
from app.presentation.api.dependencies import bearer_scheme
from app.presentation.api.schemas.responses.birthing_person import (
    BirthingPersonResponse,
    BirthingPersonSummaryResponse,
)
from app.presentation.exception_handler import ExceptionSchema
from app.setup.ioc.di_component_enum import ComponentEnum

birthing_person_router = APIRouter(prefix="/birthing-person", tags=["Birthing Person"])


@birthing_person_router.post(
    "/register",
    responses={
        status.HTTP_200_OK: {"model": BirthingPersonResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def register(
    service: Annotated[BirthingPersonService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> BirthingPersonResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    birthing_person = await service.register(
        birthing_person_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
    )
    return BirthingPersonResponse(birthing_person=birthing_person)


@birthing_person_router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": BirthingPersonResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_birthing_person(
    service: Annotated[BirthingPersonService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> BirthingPersonResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    birthing_person = await service.get_birthing_person(birthing_person_id=user.id)
    return BirthingPersonResponse(birthing_person=birthing_person)


@birthing_person_router.get(
    "/get-or-create",
    responses={
        status.HTTP_200_OK: {"model": BirthingPersonResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_or_create(
    service: Annotated[BirthingPersonService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> BirthingPersonResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    try:
        birthing_person = await service.get_birthing_person(birthing_person_id=user.id)
    except (BirthingPersonNotFoundById):
        birthing_person = await service.register(
            birthing_person_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            email=user.email,
        )
    return BirthingPersonResponse(birthing_person=birthing_person)


@birthing_person_router.get(
    "/summary",
    responses={
        status.HTTP_200_OK: {"model": BirthingPersonSummaryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_birthing_person_summary(
    service: Annotated[BirthingPersonService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> BirthingPersonSummaryResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    birthing_person = await service.get_birthing_person_summary(birthing_person_id=user.id)
    return BirthingPersonSummaryResponse(birthing_person=birthing_person)
