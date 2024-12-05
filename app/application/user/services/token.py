import logging

from app.application.user.ports.access_token_processor import (
    AccessTokenProcessorInterface,
)
from app.application.user.ports.access_token_request_handler import (
    AccessTokenRequestHandlerInterface,
)

log = logging.getLogger(__name__)


class TokenService:
    def __init__(
        self,
        access_token_processor: AccessTokenProcessorInterface,
        access_token_request_handler: AccessTokenRequestHandlerInterface,
    ):
        self._access_token_processor = access_token_processor
        self._access_token_request_handler = access_token_request_handler

    def issue_access_token(self, session_id: str) -> str:
        log.debug(f"Started. Session id: '{session_id}'.")

        access_token: str = self._access_token_processor.issue_access_token(
            session_id
        )

        log.debug(f"Done. Session id: '{session_id}'.")
        return access_token

    def add_access_token_to_request(self, access_token: str) -> None:
        self._access_token_request_handler.add_access_token_to_request(
            access_token
        )

    def delete_access_token_from_request(self) -> None:
        self._access_token_request_handler.delete_access_token_from_request()
