class RequestVerificationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class VerificationTokenAlreadyUsedException(RequestVerificationError):
    def __init__(self):
        super().__init__(message="Verification token has already been used.")


class InvalidVerificationTokenException(RequestVerificationError):
    def __init__(self):
        super().__init__(message="Verification token is invalid.")
