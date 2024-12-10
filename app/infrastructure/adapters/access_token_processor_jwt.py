from typing import Any, cast

import jwt

from app.application.adapters.access_token_processor import AccessTokenProcessor
from app.application.adapters.session_timer import SessionTimer
from app.application.exceptions import AdapterError
from app.infrastructure.custom_types import JwtAlgorithm, JwtSecret


class JwtAccessTokenProcessor(AccessTokenProcessor):
    def __init__(
        self,
        secret: JwtSecret,
        algorithm: JwtAlgorithm,
        session_timer: SessionTimer,
    ):
        self._secret = secret
        self._algorithm = algorithm
        self._session_timer = session_timer

    def issue_access_token(self, user_id: str, session_id: str) -> str:
        to_encode: dict[str, Any] = {
            "session_id": session_id,
            "user_id": user_id,
            "exp": int(self._session_timer.access_expiration.timestamp()),
        }
        return jwt.encode(
            payload=to_encode,
            key=self._secret,
            algorithm=self._algorithm,
        )

    def extract_ids(self, access_token: str) -> tuple[str, str]:
        """
        :raises AdapterError:
        """
        payload: dict[str, Any] = self._decode_token(access_token)

        session_id: str | None = payload.get("session_id")
        if session_id is None:
            raise AdapterError("Token has no Session id.")

        user_id: str | None = payload.get("user_id")
        if user_id is None:
            raise AdapterError("Token has no user id.")

        return (user_id, session_id)

    def _decode_token(self, token: str) -> dict[str, Any]:
        """
        :raises AdapterError:
        """
        try:
            return cast(
                dict[str, Any],
                jwt.decode(
                    jwt=token,
                    key=self._secret,
                    algorithms=[self._algorithm],
                ),
            )
        except jwt.PyJWTError as error:
            raise AdapterError("Token is invalid or expired.") from error
