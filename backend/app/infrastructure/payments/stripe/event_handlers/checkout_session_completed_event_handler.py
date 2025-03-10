import logging
from typing import Any

import stripe

from app.application.events.event_handler import EventHandler
from app.application.services.labour_service import LabourService
from app.domain.labour.enums import LabourPaymentPlan

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
            # TODO get purchased item
            await self._labour_service.update_labour_payment_plan(
                birthing_person_id=user_id, payment_plan=LabourPaymentPlan.COMMUNITY.value
            )
