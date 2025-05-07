from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.dependencies import bearer_scheme
from src.api.exception_handler import ExceptionSchema
from src.labour.api.schemas.requests.labour import (
    CompleteLabourRequest,
    PlanLabourRequest,
    SendInviteRequest,
)
from src.labour.api.schemas.responses.labour import (
    LabourResponse,
    LabourSubscriptionTokenResponse,
)
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_invite_service import LabourInviteService
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.application.services.labour_service import LabourService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.user.infrastructure.auth.interfaces.controller import AuthController

labour_router = APIRouter(prefix="/labour", tags=["Labour"])


@labour_router.post(
    "/plan",
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
async def plan_labour(
    request_data: PlanLabourRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.plan_labour(
        birthing_person_id=user.id,
        first_labour=request_data.first_labour,
        due_date=request_data.due_date,
        labour_name=request_data.labour_name,
    )
    return LabourResponse(labour=labour)


@labour_router.put(
    "/plan",
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
async def update_labour_plan(
    request_data: PlanLabourRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.update_labour_plan(
        birthing_person_id=user.id,
        first_labour=request_data.first_labour,
        due_date=request_data.due_date,
        labour_name=request_data.labour_name,
    )
    return LabourResponse(labour=labour)


@labour_router.post(
    "/begin",
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
async def begin_labour(
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.begin_labour(user.id)
    return LabourResponse(labour=labour)


@labour_router.put(
    "/complete",
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
async def complete_labour(
    request_data: CompleteLabourRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.complete_labour(
        birthing_person_id=user.id, end_time=request_data.end_time, notes=request_data.notes
    )
    return LabourResponse(labour=labour)


@labour_router.delete(
    "/delete/{labour_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_labour(
    labour_id: str,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    return await service.delete_labour(requester_id=user.id, labour_id=labour_id)


@labour_router.get(
    "/subscription-token",
    responses={
        status.HTTP_200_OK: {"model": LabourSubscriptionTokenResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_subscription_token(
    service: Annotated[LabourQueryService, FromComponent(ComponentEnum.LABOUR)],
    token_generator: Annotated[TokenGenerator, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourSubscriptionTokenResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.get_active_labour(birthing_person_id=user.id)
    token = token_generator.generate(input=labour.id)
    return LabourSubscriptionTokenResponse(token=token)


@labour_router.post(
    "/send_invite",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def send_invite(
    request_data: SendInviteRequest,
    labour_invite_service: Annotated[LabourInviteService, FromComponent(ComponentEnum.INVITES)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    await labour_invite_service.send_invite(
        birthing_person_id=user.id,
        labour_id=request_data.labour_id,
        invite_email=request_data.invite_email,
    )
    return None
