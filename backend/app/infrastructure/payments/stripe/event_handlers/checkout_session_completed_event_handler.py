import logging
from typing import Any

import stripe

from app.application.events.event_handler import EventHandler
from app.application.services.labour_service import LabourService
from app.domain.labour.enums import LabourPaymentPlan
from app.infrastructure.payments.stripe.product_mapping import STRIPE_PRICE_TO_PAYMENT_PLAN

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
            if len(checkout_session.line_items) > 1:
                log.error(f"Multiple line items found for checkout {session_id}")

            purchased_item = checkout_session.line_items.data[0]
            if not purchased_item.price:
                log.error(f"No price ID found for item in checkout {session_id}")
                return

            price_id = purchased_item.price.id
            new_payment_plan = STRIPE_PRICE_TO_PAYMENT_PLAN.get(price_id, None)

            if not new_payment_plan:
                log.error(f"No payment plan found for price {price_id} in checkout {session_id}")
                log.info(f"Defaulting to Community plan for checkout {session_id}")
                new_payment_plan = LabourPaymentPlan.COMMUNITY.value

            await self._labour_service.update_labour_payment_plan(
                birthing_person_id=user_id, payment_plan=new_payment_plan
            )
