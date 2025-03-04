from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from app.application.security.token_generator import TokenGenerator
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_invite_service import LabourInviteService
from app.application.services.labour_service import LabourService
from app.application.services.subscription_service import SubscriptionService
from app.infrastructure.auth.interfaces.controller import AuthController
from app.presentation.api.dependencies import bearer_scheme
from app.presentation.api.schemas.requests.contraction import (
    EndContractionRequest,
    StartContractionRequest,
    UpdateContractionRequest,
)
from app.presentation.api.schemas.requests.labour import (
    CompleteLabourRequest,
    PlanLabourRequest,
    SendInviteRequest,
)
from app.presentation.api.schemas.requests.labour_update import (
    DeleteLabourUpdateRequest,
    LabourUpdateRequest,
)
from app.presentation.api.schemas.responses.labour import (
    LabourListResponse,
    LabourResponse,
    LabourSubscriptionTokenResponse,
    LabourSummaryResponse,
)
from app.presentation.exception_handler import ExceptionSchema
from app.setup.ioc.di_component_enum import ComponentEnum

labour_router = APIRouter(prefix="/labour", tags=["Labour"])


@labour_router.get(
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
    service: Annotated[GetLabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourListResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labours = await service.get_all_labours(birthing_person_id=user.id)
    return LabourListResponse(labours=labours)


@labour_router.get(
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
    service: Annotated[GetLabourService, FromComponent(ComponentEnum.LABOUR)],
    subscription_service: Annotated[
        SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
    ],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    await subscription_service.can_user_access_labour(requester_id=user.id, labour_id=labour_id)
    labour = await service.get_labour_by_id(labour_id=labour_id)
    return LabourResponse(labour=labour)


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


@labour_router.post(
    "/contraction/start",
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
async def start_contraction(
    request_data: StartContractionRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.start_contraction(
        birthing_person_id=user.id,
        start_time=request_data.start_time,
        intensity=request_data.intensity,
        notes=request_data.notes,
    )
    return LabourResponse(labour=labour)


@labour_router.put(
    "/contraction/end",
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
async def end_contraction(
    request_data: EndContractionRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.end_contraction(
        birthing_person_id=user.id,
        intensity=request_data.intensity,
        end_time=request_data.end_time,
        notes=request_data.notes,
    )
    return LabourResponse(labour=labour)


@labour_router.put(
    "/contraction/update",
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
async def update_contraction(
    request_data: UpdateContractionRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.update_contraction(
        birthing_person_id=user.id,
        contraction_id=request_data.contraction_id,
        start_time=request_data.start_time,
        end_time=request_data.end_time,
        intensity=request_data.intensity,
        notes=request_data.notes,
    )
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
    await service.delete_labour(birthing_person_id=user.id, labour_id=labour_id)
    return


@labour_router.get(
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
    service: Annotated[GetLabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.get_active_labour(birthing_person_id=user.id)
    return LabourResponse(labour=labour)


@labour_router.get(
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
    service: Annotated[GetLabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourSummaryResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.get_active_labour_summary(birthing_person_id=user.id)
    return LabourSummaryResponse(labour=labour)


@labour_router.post(
    "/labour-update",
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
async def post_labour_update(
    request_data: LabourUpdateRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.post_labour_update(
        birthing_person_id=user.id,
        labour_update_type=request_data.labour_update_type,
        message=request_data.message,
        sent_time=request_data.sent_time,
    )
    return LabourResponse(labour=labour)


@labour_router.delete(
    "/labour-update",
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
async def delete_labour_update(
    request_data: DeleteLabourUpdateRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.delete_labour_update(
        birthing_person_id=user.id,
        labour_update_id=request_data.labour_update_id,
    )
    return LabourResponse(labour=labour)


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
    service: Annotated[GetLabourService, FromComponent(ComponentEnum.LABOUR)],
    token_generator: Annotated[TokenGenerator, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
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
    labour_invite_service: Annotated[LabourInviteService, FromComponent(ComponentEnum.LABOUR)],
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
