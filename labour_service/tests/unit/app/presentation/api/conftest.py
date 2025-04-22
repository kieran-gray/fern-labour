from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.admin.application.services.contact_service import ContactService
from src.api.exception_handler import (
    ExceptionHandler,
    ExceptionHeaderMapper,
    ExceptionMapper,
    ExceptionMessageProvider,
)
from src.api.routes.router_root import root_router
from src.common.infrastructure.security.interfaces.request_verification_service import (
    RequestVerificationService,
)
from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.security.labour_authorization_service import LabourAuthorizationService
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.application.services.labour_service import LabourService
from src.payments.infrastructure.gateways.stripe.stripe_gateway import StripePaymentService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.subscription.application.dtos.subscription import SubscriptionDTO
from src.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.user.application.dtos.user import UserDTO
from src.user.application.dtos.user_summary import UserSummaryDTO
from src.user.application.services.user_query_service import UserQueryService
from src.user.infrastructure.auth.interfaces.controller import AuthController
from src.user.infrastructure.auth.interfaces.exceptions import AuthorizationError
from src.user.infrastructure.auth.interfaces.models import AuthorizationCredentials
from src.user.infrastructure.auth.interfaces.schemas import TokenResponse


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
def mock_labour_dto() -> LabourDTO:
    """Create a mock labour DTO."""
    return LabourDTO(
        id="540a35a9-0323-41a6-b96a-334bcf566c5b",
        birthing_person_id="test_id",
        payment_plan="solo",
        start_time=None,
        end_time=None,
        first_labour=True,
        due_date=datetime(2020, 1, 1, 1),
        labour_name="Test Labour",
        current_phase="PLANNED",
        contractions=[],
        announcements=[],
        status_updates=[],
        recommendations={},
        notes=None,
    )


@pytest.fixture(scope="session")
def mock_user_summary_dto(test_user: UserDTO) -> UserSummaryDTO:
    """Create a mock user summary DTO."""
    return UserSummaryDTO(
        id=test_user.id,
        first_name=test_user.first_name,
        last_name=test_user.last_name,
    )


@pytest.fixture(scope="session")
def mock_subscription_dto(test_user: UserDTO) -> SubscriptionDTO:
    """Create a mock subscription DTO."""
    return SubscriptionDTO(
        id="test_subscription_id",
        subscriber_id=test_user.id,
        birthing_person_id="test_birthing_person_id",
        labour_id="test_labour_id",
        role="friends_and_family",
        status="subscribed",
        contact_methods=[],
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


class MockSubscriptionProvider(Provider):
    scope = Scope.REQUEST
    component = ComponentEnum.SUBSCRIPTIONS

    def get_mock_subscription(
        self,
        status: str = "subscribed",
        role: str = "friends_and_family",
        contact_methods: list[str] | None = None,
    ) -> SubscriptionDTO:
        return SubscriptionDTO(
            id="test_subscription_id",
            subscriber_id="test_id",
            birthing_person_id="test_birthing_person_id",
            labour_id="test_labour_id",
            role=role,
            status=status,
            contact_methods=contact_methods or [],
        )

    @provide()
    def get_subscription_authorization_service(self) -> SubscriptionAuthorizationService:
        """Create a mock subscription authorization service."""
        service = MagicMock(spec=SubscriptionAuthorizationService)
        service.ensure_can_view_subscription.return_value = None
        service.ensure_can_manage_as_birthing_person.return_value = None
        service.ensure_can_manage_as_subscriber.return_value = None
        service.ensure_can_access_labour.return_value = None
        return service

    @provide()
    def get_subscription_service(self) -> SubscriptionService:
        """Create a mock subscription service."""
        service = MagicMock(spec=SubscriptionService)
        service.subscribe_to.return_value = self.get_mock_subscription()
        service.unsubscribe_from.return_value = self.get_mock_subscription("unsubscribed")
        return service

    @provide()
    def get_subscription_query_service(self) -> SubscriptionQueryService:
        """Create a mock subscription query service."""
        service = MagicMock(spec=SubscriptionQueryService)
        service.get_by_id.return_value = self.get_mock_subscription()
        service.get_subscriber_subscriptions.return_value = [self.get_mock_subscription()]
        service.get_labour_subscriptions.return_value = [self.get_mock_subscription()]
        return service

    @provide()
    def get_subscription_management_service(self) -> SubscriptionManagementService:
        """Create a mock subscription management service."""
        service = MagicMock(spec=SubscriptionManagementService)
        service.remove_subscriber.return_value = self.get_mock_subscription("removed")
        service.block_subscriber.return_value = self.get_mock_subscription("blocked")
        service.update_role.return_value = self.get_mock_subscription(role="birth_partner")
        service.update_contact_methods.return_value = self.get_mock_subscription(
            contact_methods=["sms"]
        )
        return service


class MockPaymentsProvider(Provider):
    scope = Scope.REQUEST
    component = ComponentEnum.PAYMENTS

    @provide()
    def get_stripe_payment_service(self) -> StripePaymentService:
        """Create a mock stripe payment service."""
        service = MagicMock(spec=StripePaymentService)
        service.handle_webhook.return_value = None
        service.create_checkout_session.return_value = MagicMock(
            id="test_session_id",
            url="https://test.stripe.com/checkout",
        )
        return service


class MockLabourProvider(Provider):
    scope = Scope.REQUEST
    component = ComponentEnum.LABOUR

    def get_mock_labour_dto(self) -> LabourDTO:
        """Create a mock labour DTO."""
        return LabourDTO(
            id="540a35a9-0323-41a6-b96a-334bcf566c5b",
            birthing_person_id="test_id",
            payment_plan="solo",
            start_time=None,
            end_time=None,
            first_labour=True,
            due_date=datetime(2020, 1, 1, 1),
            labour_name="Test Labour",
            current_phase="PLANNED",
            contractions=[],
            announcements=[],
            status_updates=[],
            recommendations={},
            notes=None,
        )

    @provide()
    def get_labour_authorization_service(self) -> LabourAuthorizationService:
        service = MagicMock(spec=LabourAuthorizationService)
        service.ensure_can_access_labour.return_value = None
        return service

    @provide()
    def get_labour_query_service(self) -> LabourQueryService:
        """Create a mock get labour service."""
        mock_labour_dto = self.get_mock_labour_dto()
        service = MagicMock(spec=LabourQueryService)
        service.get_all_labours.return_value = [mock_labour_dto]
        service.get_labour_by_id.return_value = mock_labour_dto
        service.get_active_labour.return_value = mock_labour_dto
        return service

    @provide()
    def get_labour_service(self) -> LabourService:
        """Create a mock labour service."""
        service = MagicMock(spec=LabourService)
        mock_labour_dto = self.get_mock_labour_dto()
        service.plan_labour.return_value = mock_labour_dto
        service.update_labour_plan.return_value = mock_labour_dto
        service.begin_labour.return_value = mock_labour_dto
        service.start_contraction.return_value = mock_labour_dto
        service.end_contraction.return_value = mock_labour_dto
        return service


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


class MockAdminProvider(Provider):
    scope = Scope.REQUEST
    component = ComponentEnum.ADMIN

    @provide()
    def get_contact_service(self) -> ContactService:
        service = MagicMock(spec=ContactService)
        service.send_contact_email.return_value = None
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

    @provide()
    def get_contact_service(self) -> ContactService:
        service = MagicMock(spec=ContactService)
        service.send_contact_email.return_value = None
        return service

    @provide()
    def get_request_verification_service(self) -> RequestVerificationService:
        service = MagicMock(spec=RequestVerificationService)
        service.verify.return_value = None
        return service


def get_providers() -> Iterable[Provider]:
    return (
        MockDefaultProvider(),
        MockLabourProvider(),
        MockPaymentsProvider(),
        MockSubscriptionProvider(),
        MockUserProvider(),
        MockAdminProvider(),
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
