from src.core.application.exceptions import ApplicationError


class SubscriberInviteRateLimitExceeded(ApplicationError):
    def __init__(self) -> None:
        super().__init__("You have reached the maximum number of invites for today.")
