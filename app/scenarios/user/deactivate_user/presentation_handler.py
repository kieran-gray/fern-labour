from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Security, status

from app.presentation.http_controllers.dependencies import cookie_scheme
from app.presentation.http_controllers.exception_handler import ExceptionSchema
from app.scenarios.user.base.application_payload import UserResponse
from app.scenarios.user.deactivate_user.application_interactor import (
    DeactivateUserInteractor,
)
from app.scenarios.user.deactivate_user.application_payload import (
    DeactivateUserRequest,
)
from app.scenarios.user.deactivate_user.presentation_schemas import (
    DeactivateUserRequestPydantic,
)

deactivate_user_router = APIRouter()


@deactivate_user_router.patch(
    "/deactivate",
    responses={
        status.HTTP_200_OK: {"model": UserResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def deactivate_user(
    request_data_pydantic: DeactivateUserRequestPydantic,
    interactor: FromDishka[DeactivateUserInteractor],
    _token_marker: str = Security(cookie_scheme),
) -> UserResponse:
    # :raises AuthenticationError:
    # :raises AuthorizationError:
    # :raises UserNotFoundByUsername:
    # :raises GatewayError:
    request_data: DeactivateUserRequest = DeactivateUserRequest(
        username=request_data_pydantic.username,
    )
    return await interactor(request_data)
