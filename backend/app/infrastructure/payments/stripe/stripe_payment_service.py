import logging
from collections.abc import Mapping

import stripe
from stripe.checkout import Session

from app.application.dtos.user import UserDTO
from app.application.events.event_handler import EventHandler
from app.infrastructure.payments.stripe.exceptions import (
    WebhookHasInvalidPayload,
    WebhookHasInvalidSignature,
    WebhookMissingSignatureHeader,
)
from app.infrastructure.payments.stripe.product_mapping import STRIPE_PRODUCT_TO_PRICE

log = logging.getLogger(__name__)


class StripePaymentService:
    def __init__(
        self, api_key: str, webhook_endpoint_secret: str, event_handlers: Mapping[str, EventHandler]
    ) -> None:
        self._api_key = api_key
        self._webhook_endpoint_secret = webhook_endpoint_secret
        self._stripe = stripe
        self._stripe.api_key = self._api_key
        self._event_handlers = event_handlers

    async def handle_webhook(self, payload: bytes, signature_header: str | None) -> None:
        if not signature_header:
            raise WebhookMissingSignatureHeader()
        try:
            event = self._stripe.Webhook.construct_event(  # type: ignore
                payload=payload, sig_header=signature_header, secret=self._webhook_endpoint_secret
            )
        except ValueError:
            raise WebhookHasInvalidPayload()
        except stripe.error.SignatureVerificationError:  # type: ignore
            raise WebhookHasInvalidSignature()

        if event_handler := self._event_handlers.get(event["type"]):
            await event_handler.handle(event=event)
        else:
            log.info(f"Received {event['type']} event. Ignoring: No Event Handler Defined.")

        return None

    async def create_checkout_session(
        self, user: UserDTO, success_url: str, cancel_url: str, item: str, labour_id: str
    ) -> Session:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": STRIPE_PRODUCT_TO_PRICE[item],
                    "quantity": 1,
                },
            ],
            customer_email=user.email,
            metadata={"user_id": user.id, "labour_id": labour_id},
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            automatic_tax={"enabled": True},
            allow_promotion_codes=True,
        )
        return checkout_session
