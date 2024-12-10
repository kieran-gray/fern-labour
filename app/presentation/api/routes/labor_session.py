from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from app.application.dtos.requests.labor_session import (
    CompleteLaborSessionRequest,
    EndContractionRequest,
    StartContractionRequest,
    StartLaborSessionRequest,
)
from app.application.dtos.responses.labor_session import (
    CompleteLaborSessionResponse,
    EndContractionResponse,
    StartContractionResponse,
    StartLaborSessionResponse,
)
from app.application.services.labor_session_service import LaborSessionService
from app.presentation.exception_handler import ExceptionSchema

labor_router = APIRouter(prefix="/labor", tags=["Labor Tracking"])


@labor_router.post(
    "/sessions",
    responses={
        status.HTTP_200_OK: {"model": StartLaborSessionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def start_labor_session(
    request_data: StartLaborSessionRequest, service: FromDishka[LaborSessionService]
) -> StartLaborSessionResponse:
    """Start a new labor session for the current user"""
    session = await service.start_labor_session(request_data.user_id, request_data.first_labor)
    return StartLaborSessionResponse(labor_session=session)


@labor_router.post(
    "/sessions/contractions",
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
    request_data: StartContractionRequest, service: FromDishka[LaborSessionService]
) -> StartContractionResponse:
    """Start a new contraction in the given labor session"""
    contraction = await service.start_contraction(
        session_id=request_data.session_id,
        intensity=request_data.intensity,
        notes=request_data.notes,
    )
    return StartContractionResponse(contraction=contraction)


@labor_router.put(
    "/sessions/contractions/current/end",
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
    request_data: EndContractionRequest, service: FromDishka[LaborSessionService]
) -> EndContractionResponse:
    """End the currently active contraction in the given session"""
    contraction = await service.end_contraction(request_data.session_id)
    return EndContractionResponse(contraction=contraction)


@labor_router.put(
    "/sessions/complete",
    responses={
        status.HTTP_200_OK: {"model": CompleteLaborSessionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def complete_session(
    request_data: CompleteLaborSessionRequest, service: FromDishka[LaborSessionService]
) -> CompleteLaborSessionResponse:
    """Mark a labor session as complete"""
    session = await service.complete_session(
        session_id=request_data.session_id, notes=request_data.notes
    )
    CompleteLaborSessionResponse(labor_session=session)
