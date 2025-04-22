from src.core.application.exceptions import ApplicationError


class UnauthorizedWebhookRequest(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Unauthorized Request: request failed verification.")
