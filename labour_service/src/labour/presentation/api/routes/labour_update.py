from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.dependencies import bearer_scheme
from src.api.exception_handler import ExceptionSchema
from src.labour.application.services.labour_service import LabourService
from src.labour.presentation.api.schemas.requests.labour_update import (
    DeleteLabourUpdateRequest,
    LabourUpdateRequest,
)
from src.labour.presentation.api.schemas.responses.labour import (
    LabourResponse,
)
from src.setup.ioc.di_component_enum import ComponentEnum
from src.user.infrastructure.auth.interfaces.controller import AuthController

labour_update_router = APIRouter(prefix="/labour/labour-update", tags=["Labour Updates"])


@labour_update_router.post(
    "/",
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


@labour_update_router.delete(
    "/",
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
