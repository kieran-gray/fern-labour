import logging
from typing import Any

import stripe

from app.common.application.event_handler import EventHandler
from app.labour.application.services.labour_service import LabourService
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.payments.infrastructure.gateways.stripe.product_mapping import (
    STRIPE_PRODUCT_TO_PAYMENT_PLAN,
    Product,
)

log = logging.getLogger(__name__)


class CheckoutSessionCompletedEventHandler(EventHandler):
    def __init__(self, api_key: str, labour_service: LabourService) -> None:
        self._stripe = stripe
        self._stripe.api_key = api_key
        self._labour_service = labour_service

    async def handle(self, event: dict[str, Any]) -> None:
        session_id = event["data"]["object"]["id"]
        user_id = event["data"]["object"]["metadata"]["user_id"]

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
                product = Product.UPGRADE_TO_COMMUNITY.value

            new_payment_plan = STRIPE_PRODUCT_TO_PAYMENT_PLAN.get(product)
            if not new_payment_plan:
                log.error(f"No payment plan found for {product} in checkout {session_id}")
                log.info(f"Defaulting to Community plan for checkout {session_id}")
                new_payment_plan = LabourPaymentPlan.COMMUNITY.value

            await self._labour_service.update_labour_payment_plan(
                birthing_person_id=user_id, payment_plan=new_payment_plan
            )
