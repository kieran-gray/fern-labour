class AuthorizationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidTokenError(AuthorizationError):
    pass
