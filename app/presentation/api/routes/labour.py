from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status

from app.application.dtos.requests.contraction import EndContractionRequest, StartContractionRequest
from app.application.dtos.requests.labour import BeginLabourRequest, CompleteLabourRequest
from app.application.dtos.responses.labour import (
    BeginLabourResponse,
    CompleteLabourResponse,
    EndContractionResponse,
    GetActiveLabourResponse,
    GetActiveLabourSummaryResponse,
    StartContractionResponse,
)
from app.application.services.labour_service import LabourService
from app.infrastructure.custom_types import KeycloakUser
from app.presentation.api.auth import get_user_info
from app.presentation.exception_handler import ExceptionSchema

labour_router = APIRouter(prefix="/labour", tags=["Labour Tracking"])


@labour_router.post(
    "/begin",
    responses={
        status.HTTP_200_OK: {"model": BeginLabourRequest},
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
    service: FromDishka[LabourService],
    user: KeycloakUser = Depends(get_user_info),
) -> BeginLabourResponse:
    """Begin labour for the current user"""
    labour = await service.begin_labour(user.id, request_data.first_labour)
    return BeginLabourResponse(labour=labour)


@labour_router.post(
    "/contraction/start",
    responses={
        status.HTTP_200_OK: {"model": StartContractionResponse},
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
    service: FromDishka[LabourService],
    user: KeycloakUser = Depends(get_user_info),
) -> StartContractionResponse:
    """Start a new contraction in the given labor session"""
    labour = await service.start_contraction(
        birthing_person_id=user.id,
        start_time=request_data.start_time,
        intensity=request_data.intensity,
        notes=request_data.notes,
    )
    return StartContractionResponse(labour=labour)


@labour_router.put(
    "/contraction/end",
    responses={
        status.HTTP_200_OK: {"model": EndContractionResponse},
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
    service: FromDishka[LabourService],
    user: KeycloakUser = Depends(get_user_info),
) -> EndContractionResponse:
    """End the currently active contraction in the given session"""
    labour = await service.end_contraction(
        birthing_person_id=user.id,
        intensity=request_data.intensity,
        end_time=request_data.end_time,
        notes=request_data.notes,
    )
    return EndContractionResponse(labour=labour)


@labour_router.put(
    "/complete",
    responses={
        status.HTTP_200_OK: {"model": CompleteLabourResponse},
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
    service: FromDishka[LabourService],
    user: KeycloakUser = Depends(get_user_info),
) -> CompleteLabourResponse:
    """Mark a labor session as complete"""
    labour = await service.complete_labour(
        birthing_person_id=user.id, end_time=request_data.end_time, notes=request_data.notes
    )
    return CompleteLabourResponse(labour=labour)


@labour_router.get(
    "/active",
    responses={
        status.HTTP_200_OK: {"model": GetActiveLabourResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_active_labour(
    service: FromDishka[LabourService],
    user: KeycloakUser = Depends(get_user_info),
) -> GetActiveLabourResponse:
    labour = await service.get_active_labour(birthing_person_id=user.id)
    return GetActiveLabourResponse(labour=labour)


@labour_router.get(
    "/active/summary",
    responses={
        status.HTTP_200_OK: {"model": GetActiveLabourSummaryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_active_labour_summary(
    service: FromDishka[LabourService],
    user: KeycloakUser = Depends(get_user_info),
) -> GetActiveLabourSummaryResponse:
    labour = await service.get_active_labour_summary(birthing_person_id=user.id)
    return GetActiveLabourSummaryResponse(labour=labour)
