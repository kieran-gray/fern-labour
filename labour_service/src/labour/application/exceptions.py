from fern_labour_core.exceptions.application import ApplicationError


class LabourInviteRateLimitExceeded(ApplicationError):
    def __init__(self) -> None:
        super().__init__("You have reached the maximum number of invites for today.")


class InvalidLabourUpdateRequest(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Invalid Labour Update Request")
