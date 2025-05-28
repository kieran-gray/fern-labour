from fern_labour_core.exceptions.application import ApplicationError


class UnauthorizedWebhookRequest(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Unauthorized Request: request failed verification.")


class CannotGenerateNotificationContent(ApplicationError):
    def __init__(self, message: str) -> None:
        super().__init__(f"Cannot generate notification content: {message}")
