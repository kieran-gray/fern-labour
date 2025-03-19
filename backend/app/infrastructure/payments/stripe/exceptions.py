class RequestVerificationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class WebhookMissingSignatureHeader(RequestVerificationError):
    def __init__(self) -> None:
        super().__init__("Missing Signature Header.")


class WebhookHasInvalidPayload(RequestVerificationError):
    def __init__(self) -> None:
        super().__init__("Webhook has invalid payload.")


class WebhookHasInvalidSignature(RequestVerificationError):
    def __init__(self) -> None:
        super().__init__("Webhook has invalid signature.")


class StripeProductNotFound(RequestVerificationError):
    def __init__(self) -> None:
        super().__init__("Requested product does not exist in Stripe.")
