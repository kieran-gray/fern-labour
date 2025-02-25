from fastapi import status

from app.domain.user.exceptions import UserNotFoundById
from app.infrastructure.auth.interfaces.exceptions import InvalidTokenError
from app.presentation.exception_handler import ExceptionHeaderMapper, ExceptionMapper


def test_domain_exception_raises_http_error():
    exception_mapper = ExceptionMapper()
    assert exception_mapper.get_status_code(UserNotFoundById("test")) == status.HTTP_404_NOT_FOUND


def test_auth_exception_returns_headers():
    exception_header_mapper = ExceptionHeaderMapper()
    assert exception_header_mapper.get_headers(InvalidTokenError("test")) == {
        "WWW-Authenticate": "Bearer"
    }
