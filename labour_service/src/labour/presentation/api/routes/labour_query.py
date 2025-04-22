from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.dependencies import bearer_scheme
from src.api.exception_handler import ExceptionSchema
from src.labour.application.security.labour_authorization_service import LabourAuthorizationService
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.domain.labour.exceptions import UnauthorizedLabourRequest
from src.labour.presentation.api.schemas.responses.labour import (
    LabourListResponse,
    LabourResponse,
    LabourSummaryResponse,
)
from src.setup.ioc.di_component_enum import ComponentEnum
from src.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from src.user.infrastructure.auth.interfaces.controller import AuthController

labour_query_router = APIRouter(prefix="/labour", tags=["Labour Queries"])


@labour_query_router.get(
    "/get-all",
    responses={
        status.HTTP_200_OK: {"model": LabourListResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_labours(
    service: Annotated[LabourQueryService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourListResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labours = await service.get_all_labours(birthing_person_id=user.id)
    return LabourListResponse(labours=labours)


@labour_query_router.get(
    "/get/{labour_id}",
    responses={
        status.HTTP_200_OK: {"model": LabourResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_labour_by_id(
    labour_id: str,
    service: Annotated[LabourQueryService, FromComponent(ComponentEnum.LABOUR)],
    subscription_authorization_service: Annotated[
        SubscriptionAuthorizationService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
    ],
    labour_authorization_service: Annotated[
        LabourAuthorizationService, FromComponent(ComponentEnum.LABOUR)
    ],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.get_labour_by_id(labour_id=labour_id)
    try:
        await labour_authorization_service.ensure_can_access_labour(
            requester_id=user.id, labour=labour
        )
    except UnauthorizedLabourRequest:
        await subscription_authorization_service.ensure_can_access_labour(
            requester_id=user.id, labour_id=labour.id
        )

    return LabourResponse(labour=labour)


@labour_query_router.get(
    "/active",
    responses={
        status.HTTP_200_OK: {"model": LabourResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_active_labour(
    service: Annotated[LabourQueryService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.get_active_labour(birthing_person_id=user.id)
    return LabourResponse(labour=labour)


@labour_query_router.get(
    "/active/summary",
    responses={
        status.HTTP_200_OK: {"model": LabourSummaryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_active_labour_summary(
    service: Annotated[LabourQueryService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourSummaryResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.get_active_labour_summary(birthing_person_id=user.id)
    return LabourSummaryResponse(labour=labour)
