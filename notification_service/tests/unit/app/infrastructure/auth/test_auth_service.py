from unittest.mock import Mock

import pytest
from keycloak import KeycloakAuthenticationError

from src.user.application.dtos.user import UserDTO
from src.user.infrastructure.auth.interfaces.exceptions import AuthorizationError, InvalidTokenError
from src.user.infrastructure.auth.keycloak.auth_service import KeycloakAuthService


def test_can_authenticate_user():
    auth_mock = Mock()
    auth_mock.token.return_value = {"access_token": "123"}

    auth_service = KeycloakAuthService(keycloak_openid=auth_mock)

    token = auth_service.authenticate_user("username", "password")
    assert token == "123"


def test_failed_authentication_raises_exception():
    auth_mock = Mock()
    auth_mock.token.side_effect = KeycloakAuthenticationError()

    auth_service = KeycloakAuthService(keycloak_openid=auth_mock)

    with pytest.raises(AuthorizationError):
        auth_service.authenticate_user("username", "password")


def test_can_verify_token():
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

    user = auth_service.verify_token("123")
    assert isinstance(user, UserDTO)
    assert user.id == "123"


def test_missing_user_info_raises_error():
    auth_mock = Mock()
    auth_mock.userinfo.return_value = None

    auth_service = KeycloakAuthService(keycloak_openid=auth_mock)

    with pytest.raises(InvalidTokenError):
        auth_service.verify_token("123")


def test_invalid_credentials_raises_error():
    auth_mock = Mock()
    auth_mock.userinfo.side_effect = KeycloakAuthenticationError()

    auth_service = KeycloakAuthService(keycloak_openid=auth_mock)

    with pytest.raises(AuthorizationError):
        auth_service.verify_token("123")
