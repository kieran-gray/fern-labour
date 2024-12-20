
from app.application.base.exceptions import ApplicationError


class AuthenticationError(ApplicationError):
    pass


class AuthorizationError(ApplicationError):
    pass
