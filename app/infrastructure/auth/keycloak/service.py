from typing import Any

from app.infrastructure.auth.interfaces.exceptions import AuthorizationError, InvalidTokenError
from app.infrastructure.auth.interfaces.models import User
from keycloak import KeycloakOpenID  # type: ignore
from keycloak.exceptions import KeycloakAuthenticationError


class KeycloakAuthService:
    def __init__(self, keycloak_openid: KeycloakOpenID):
        self._keycloak_openid = keycloak_openid

    def authenticate_user(self, username: str, password: str) -> str:
        """
        Authenticate the user using Keycloak and return an access token.
        """
        try:
            token = self._keycloak_openid.token(username, password)
            return token["access_token"]  # type: ignore
        except KeycloakAuthenticationError:
            raise AuthorizationError("Invalid username or password")

    def verify_token(self, token: str) -> User:
        """
        Verify the given token and return user information.
        """
        try:
            user_info = self._keycloak_openid.userinfo(token)
            if not user_info:
                raise InvalidTokenError("Invalid token")
            return self._to_user(user_info=user_info)
        except KeycloakAuthenticationError:
            raise AuthorizationError("Could not validate credentials")

    def _to_user(self, user_info: dict[str, Any]) -> User:
        return User(
            id=user_info.get("sub"),  # type: ignore
            username=user_info.get("preferred_username"),  # type: ignore
            email=user_info.get("email"),  # type: ignore
            first_name=user_info.get("given_name"),  # type: ignore
            last_name=user_info.get("family_name"),  # type: ignore
            phone_number=user_info.get("phone_number"),
        )
