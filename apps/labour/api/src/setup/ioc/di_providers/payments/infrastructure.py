import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.payments.infrastructure.stripe.stripe_payment_service import (
    StripePaymentService,
)
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)

log = logging.getLogger(__name__)


class PaymentsInfrastructureProvider(Provider):
    component = ComponentEnum.PAYMENTS
    scope = Scope.REQUEST

    @provide()
    def provide_stripe_payment_service(
        self,
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
        subscription_management_service: Annotated[
            SubscriptionManagementService, FromComponent(ComponentEnum.SUBSCRIPTION)
        ],
    ) -> StripePaymentService:
        return StripePaymentService(
            api_key=settings.payments.stripe.api_key,
            webhook_endpoint_secret=settings.payments.stripe.webhook_endpoint_secret,
            subscription_management_service=subscription_management_service,
        )
