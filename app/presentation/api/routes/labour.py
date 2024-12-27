from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status

from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_service import LabourService
from app.infrastructure.custom_types import KeycloakUser
from app.presentation.api.auth import get_user_info
from app.presentation.api.schemas.requests.contraction import (
    EndContractionRequest,
    StartContractionRequest,
)
from app.presentation.api.schemas.requests.labour import BeginLabourRequest, CompleteLabourRequest
from app.presentation.api.schemas.responses.labour import LabourResponse, LabourSummaryResponse
from app.presentation.exception_handler import ExceptionSchema
from app.setup.ioc.di_component_enum import ComponentEnum

labour_router = APIRouter(prefix="/labour", tags=["Labour Tracking"])


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
    request_data: BeginLabourRequest,
    service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    user: KeycloakUser = Depends(get_user_info),
) -> LabourResponse:
    """Begin labour for the current user"""
    labour = await service.begin_labour(user.id, request_data.first_labour)
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
    user: KeycloakUser = Depends(get_user_info),
) -> LabourResponse:
    """Start a new contraction in the given labor session"""
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
    user: KeycloakUser = Depends(get_user_info),
) -> LabourResponse:
    """End the currently active contraction in the given session"""
    labour = await service.end_contraction(
        birthing_person_id=user.id,
        intensity=request_data.intensity,
        end_time=request_data.end_time,
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
    user: KeycloakUser = Depends(get_user_info),
) -> LabourResponse:
    """Mark a labor session as complete"""
    labour = await service.complete_labour(
        birthing_person_id=user.id, end_time=request_data.end_time, notes=request_data.notes
    )
    return LabourResponse(labour=labour)


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
    user: KeycloakUser = Depends(get_user_info),
) -> LabourResponse:
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
    user: KeycloakUser = Depends(get_user_info),
) -> LabourSummaryResponse:
    labour = await service.get_active_labour_summary(birthing_person_id=user.id)
    return LabourSummaryResponse(labour=labour)
