from unittest.mock import Mock

from src.user.application.dtos.user import UserDTO
from src.user.infrastructure.auth.interfaces.models import AuthorizationCredentials
from src.user.infrastructure.auth.interfaces.schemas import TokenResponse
from src.user.infrastructure.auth.keycloak.auth_controller import KeycloakAuthController
from src.user.infrastructure.auth.keycloak.auth_service import KeycloakAuthService


class MockAuthorizationCredentials(AuthorizationCredentials):
    def __init__(self, scheme: str, credentials: str) -> None:
        self.scheme = scheme
        self.credentials = credentials


def test_can_login():
    auth_service_mock = Mock()
    auth_service_mock.authenticate_user.return_value = "123"

    auth_controller = KeycloakAuthController(auth_service=auth_service_mock)

    token = auth_controller.login("username", "password")

    assert isinstance(token, TokenResponse)
    assert token.access_token == "123"
    assert token.token_type == "bearer"


def test_can_get_authenticated_user():
    auth_mock = Mock()
    auth_mock.userinfo.return_value = {
        "sub": "123",
        "preferred_username": "test",
        "email": "email@test.com",
        "given_name": "first",
        "family_name": "last",
        "phone_number": "12312312301",
    }
    auth_service = KeycloakAuthService(keycloak_openid=auth_mock)

    auth_controller = KeycloakAuthController(auth_service=auth_service)

    creds = MockAuthorizationCredentials("test", "test")

    user = auth_controller.get_authenticated_user(credentials=creds)

    assert isinstance(user, UserDTO)
