import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.labour.application.services.labour_service import LabourService
from app.payments.application.event_handlers.checkout_session_completed_event_handler import (
    CheckoutSessionCompletedEventHandler,
)
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings

log = logging.getLogger(__name__)


class PaymentEventsApplicationProvider(Provider):
    component = ComponentEnum.PAYMENT_EVENTS
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
