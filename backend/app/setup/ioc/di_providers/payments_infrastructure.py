import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.labour.application.services.labour_service import LabourService
from app.payments.application.event_handlers.checkout_session_completed_event_handler import (  # noqa: E501
    CheckoutSessionCompletedEventHandler,
)
from app.payments.infrastructure.gateways.stripe.stripe_gateway import StripePaymentService
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings

log = logging.getLogger(__name__)


class PaymentsInfrastructureProvider(Provider):
    component = ComponentEnum.PAYMENTS
    scope = Scope.REQUEST

    @provide()
    def provide_checkout_session_completed_event_handler(
        self,
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
        labour_service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    ) -> CheckoutSessionCompletedEventHandler:
        return CheckoutSessionCompletedEventHandler(
            api_key=settings.payments.stripe.api_key, labour_service=labour_service
        )

    @provide()
    def provide_stripe_payment_service(
        self,
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
        checkout_completed_event_handler: CheckoutSessionCompletedEventHandler,
    ) -> StripePaymentService:
        event_mapping = {
            "checkout.session.completed": checkout_completed_event_handler,
            "checkout.session.async_payment_succeeded": checkout_completed_event_handler,
        }
        return StripePaymentService(
            api_key=settings.payments.stripe.api_key,
            webhook_endpoint_secret=settings.payments.stripe.webhook_endpoint_secret,
            event_handlers=event_mapping,
        )
