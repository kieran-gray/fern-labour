import secrets

from app.application.user.ports.session_id_generator import (
    SessionIdGeneratorInterface,
)


class StrSessionIdGenerator(SessionIdGeneratorInterface):
    def __call__(self) -> str:
        return secrets.token_urlsafe(32)
