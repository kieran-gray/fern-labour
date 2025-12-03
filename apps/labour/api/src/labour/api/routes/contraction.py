from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.dependencies import bearer_scheme
from src.api.exception_handler import ExceptionSchema
from src.labour.api.schemas.requests.contraction import (
    DeleteContractionRequest,
    EndContractionRequest,
    StartContractionRequest,
    UpdateContractionRequest,
)
from src.labour.api.schemas.responses.labour import (
    LabourResponse,
)
from src.labour.application.services.contraction_service import ContractionService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.user.infrastructure.auth.interfaces.controller import AuthController

contraction_router = APIRouter(prefix="/labour/contraction", tags=["Contractions"])


@contraction_router.post(
    "/start",
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
    service: Annotated[ContractionService, FromComponent(ComponentEnum.LABOUR)],
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


@contraction_router.put(
    "/end",
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
    service: Annotated[ContractionService, FromComponent(ComponentEnum.LABOUR)],
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


@contraction_router.put(
    "/update",
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
    service: Annotated[ContractionService, FromComponent(ComponentEnum.LABOUR)],
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


@contraction_router.delete(
    "/delete",
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
async def delete_contraction(
    request_data: DeleteContractionRequest,
    service: Annotated[ContractionService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await service.delete_contraction(
        birthing_person_id=user.id,
        contraction_id=request_data.contraction_id,
    )
    return LabourResponse(labour=labour)
