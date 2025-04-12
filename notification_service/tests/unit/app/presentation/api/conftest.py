from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.exception_handler import (
    ExceptionHandler,
    ExceptionHeaderMapper,
    ExceptionMapper,
    ExceptionMessageProvider,
)
from app.api.routes.router_root import root_router
from app.setup.ioc.di_component_enum import ComponentEnum
from app.user.application.dtos.user import UserDTO
from app.user.application.dtos.user_summary import UserSummaryDTO
from app.user.application.services.user_query_service import UserQueryService
from app.user.infrastructure.auth.interfaces.controller import AuthController
from app.user.infrastructure.auth.interfaces.exceptions import AuthorizationError
from app.user.infrastructure.auth.interfaces.models import AuthorizationCredentials
from app.user.infrastructure.auth.interfaces.schemas import TokenResponse


@pytest.fixture(scope="session")
def test_user() -> UserDTO:
    return UserDTO(
        id="test_id",
        username="test_user",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        phone_number="",
    )


@pytest.fixture(scope="session")
def mock_user_summary_dto(test_user: UserDTO) -> UserSummaryDTO:
    """Create a mock user summary DTO."""
    return UserSummaryDTO(
        id=test_user.id,
        first_name=test_user.first_name,
        last_name=test_user.last_name,
    )


@dataclass
class TestAuthorizationCredentials:
    """Test implementation of AuthorizationCredentials."""

    scheme: str
    credentials: str


class TestAuthController(AuthController):
    """Test implementation of AuthController."""

    def __init__(self, test_user: UserDTO | None = None, test_token: str | None = None) -> None:
        """Initialize the test auth controller with optional test user and token."""
        self._test_user = test_user or UserDTO(
            id="test_id",
            username="test_user",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        self._test_token = test_token or "test_token"
        self._valid_credentials = {
            "test_user": "test_password",
        }

    def login(self, username: str, password: str) -> TokenResponse:
        """
        Test implementation of login.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user.

        Raises:
            AuthorizationError: If the authentication fails (wrong credentials).

        Returns:
            TokenResponse: Contains the access token upon successful authentication.
        """
        if username not in self._valid_credentials or self._valid_credentials[username] != password:
            raise AuthorizationError("Invalid username or password")

        return TokenResponse(access_token=self._test_token, token_type="Bearer")

    def get_authenticated_user(self, credentials: AuthorizationCredentials) -> UserDTO:
        """
        Test implementation of get_authenticated_user.

        Args:
            credentials (AuthorizationCredentials):
                Bearer token provided via HTTP Authorization header.

        Raises:
            AuthorizationError: If the token is invalid or not provided.

        Returns:
            User: Information about the authenticated user.
        """
        if credentials.scheme.lower() != "bearer" or credentials.credentials != self._test_token:
            raise AuthorizationError("Could not validate credentials")

        return self._test_user


class MockUserProvider(Provider):
    scope = Scope.REQUEST
    component = ComponentEnum.USER

    @provide()
    def get_user_service(self) -> UserQueryService:
        test_user = UserDTO(
            id="test_id",
            username="test_user",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone_number="",
        )
        service = MagicMock(spec=UserQueryService)
        service.get.return_value = test_user
        service.get_many.return_value = [test_user]
        service.get_summary.return_value = test_user.to_summary()
        service.get_many_summary.return_value = [test_user.to_summary()]
        return service


class MockDefaultProvider(Provider):
    scope = Scope.REQUEST
    component = ComponentEnum.DEFAULT

    @provide(scope=Scope.APP)
    def get_auth_controller(self) -> AuthController:
        test_user = UserDTO(
            id="test_id",
            username="test_user",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone_number="",
        )
        auth_controller = TestAuthController(test_user=test_user)
        return auth_controller


def get_providers() -> Iterable[Provider]:
    return (
        MockDefaultProvider(),
        MockUserProvider(),
    )


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Create a test FastAPI application."""
    new_app: FastAPI = FastAPI()
    new_app.include_router(root_router)
    exception_message_provider = ExceptionMessageProvider()
    exception_mapper = ExceptionMapper()
    exception_header_mapper = ExceptionHeaderMapper()
    exception_handler = ExceptionHandler(
        new_app, exception_message_provider, exception_mapper, exception_header_mapper
    )
    exception_handler.setup_handlers()
    return new_app


@pytest_asyncio.fixture(scope="session")
async def container():
    """Create a test dishka container."""
    container = make_async_container(*get_providers())
    yield container
    await container.close()


@pytest.fixture(scope="session")
def client(app: FastAPI, container: Iterator[AsyncContainer]) -> Iterator[TestClient]:
    """Create a test client for the FastAPI application."""
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client
