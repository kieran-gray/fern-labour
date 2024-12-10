import logging
from uuid import UUID

from app.application.adapters.access_token_processor import AccessTokenProcessor
from app.application.adapters.access_token_request_handler import AccessTokenRequestHandler

log = logging.getLogger(__name__)


class TokenService:
    def __init__(
        self,
        access_token_processor: AccessTokenProcessor,
        access_token_request_handler: AccessTokenRequestHandler,
    ):
        self._access_token_processor = access_token_processor
        self._access_token_request_handler = access_token_request_handler

    def issue_access_token(self, user_id: UUID, session_id: UUID) -> str:
        access_token: str = self._access_token_processor.issue_access_token(
            user_id=str(user_id),
            session_id=str(session_id)
        )
        return access_token

    def add_access_token_to_request(self, access_token: str) -> None:
        self._access_token_request_handler.add_access_token_to_request(access_token)

    def delete_access_token_from_request(self) -> None:
        self._access_token_request_handler.delete_access_token_from_request()
