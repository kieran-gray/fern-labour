from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Security, status

from app.presentation.http_controllers.dependencies import cookie_scheme
from app.presentation.http_controllers.exception_handler import ExceptionSchema
from app.scenarios.user.get_own_user.application_interactor import (
    GetOwnUserInteractor,
)
from app.scenarios.user.get_own_user.application_payload import (
    GetOwnUserResponse,
)

get_own_user_router = APIRouter()


@get_own_user_router.get(
    "/me",
    responses={
        status.HTTP_200_OK: {"model": GetOwnUserResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_own_user(
    interactor: FromDishka[GetOwnUserInteractor],
    _token_marker: str = Security(cookie_scheme),
) -> GetOwnUserResponse:
    # :raises AuthenticationError:
    # :raises AuthorizationError:
    # :raises GatewayError:
    return await interactor()
