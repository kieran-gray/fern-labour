import logging
from typing import Any

import stripe
from stripe.checkout import Session

from src.payments.infrastructure.stripe.exceptions import (
    StripeProductNotFound,
    WebhookHasInvalidPayload,
    WebhookHasInvalidSignature,
    WebhookMissingSignatureHeader,
)
from src.payments.infrastructure.stripe.product_mapping import (
    STRIPE_PRODUCT_TO_ACCESS_LEVEL,
    Product,
)
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.domain.enums import SubscriptionAccessLevel
from src.user.application.dtos.user import UserDTO

log = logging.getLogger(__name__)


class StripePaymentService:
    def __init__(
        self,
        api_key: str,
        webhook_endpoint_secret: str,
        subscription_management_service: SubscriptionManagementService,
    ) -> None:
        self._api_key = api_key
        self._webhook_endpoint_secret = webhook_endpoint_secret
        self._subscription_management_service = subscription_management_service
        self._stripe = stripe
        self._stripe.api_key = self._api_key
        self._completed_checkout_events = {
            "checkout.session.completed",
            "checkout.session.async_payment_succeeded",
        }

    async def generate_line_item(self, item: str) -> Session.CreateParamsLineItem:
        products = await stripe.Product.list_async(active=True)
        for product in products.data:
            if product.metadata.get("product") == item:
                # Casting to str for typing, it will be a str unless expanded.
                return {"price": str(product.default_price), "quantity": 1}
        raise StripeProductNotFound()

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

        if event["type"] in self._completed_checkout_events:
            await self.complete_checkout_session(event=event)
        else:
            log.info(f"Received {event['type']} event. Ignoring.")

        return None

    async def complete_checkout_session(self, event: dict[str, Any]) -> None:
        session_id = event["data"]["object"]["id"]
        subscription_id = event["data"]["object"]["metadata"]["subscription_id"]

        log.info(f"Fulfilling checkout session: {session_id}")
        checkout_session = self._stripe.checkout.Session.retrieve(session_id, expand=["line_items"])
        if checkout_session.payment_status != "unpaid":
            if not checkout_session.line_items:
                log.error(f"No line items found for checkout {session_id}")
                return

            if len(checkout_session.line_items.data) > 1:
                log.error(f"Multiple line items found for checkout {session_id}")

            purchased_item = checkout_session.line_items.data[0]
            if not purchased_item.price:
                log.error(f"No price ID found for item in checkout {session_id}")
                return

            # Casting to str for typing, it will be a str unless expanded.
            stripe_product = await self._stripe.Product.retrieve_async(
                id=str(purchased_item.price.product)
            )

            product = stripe_product.metadata.get("product")
            if not product:
                log.error(
                    f"No product metadata for price {stripe_product.id} in checkout {session_id}"
                )
                log.info(f"Defaulting to Community plan for checkout {session_id}")
                product = Product.UPGRADE_TO_SUPPORTER.value

            access_level = STRIPE_PRODUCT_TO_ACCESS_LEVEL.get(product)
            if not access_level:
                log.error(f"No access level found for {product} in checkout {session_id}")
                log.info(f"Defaulting to Supporter access level for checkout {session_id}")
                access_level = SubscriptionAccessLevel.SUPPORTER.value

            await self._subscription_management_service.update_access_level(
                subscription_id=subscription_id, access_level=access_level
            )

    async def create_checkout_session(
        self, user: UserDTO, success_url: str, cancel_url: str, item: str, subscription_id: str
    ) -> Session:
        line_item = await self.generate_line_item(item=item)
        checkout_session = stripe.checkout.Session.create(
            line_items=[line_item],
            customer_email=user.email,
            metadata={"user_id": user.id, "subscription_id": subscription_id},
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            automatic_tax={"enabled": True},
            allow_promotion_codes=True,
        )
        return checkout_session
