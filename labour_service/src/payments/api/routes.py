from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.dependencies import bearer_scheme
from src.api.exception_handler import ExceptionSchema
from src.labour.application.services.labour_service import LabourService
from src.payments.api.requests import CreateCheckoutRequest
from src.payments.api.responses import CheckoutResponse
from src.payments.infrastructure.gateways.stripe.product_mapping import Product
from src.payments.infrastructure.gateways.stripe.stripe_gateway import StripePaymentService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.user.infrastructure.auth.interfaces.controller import AuthController

payments_router = APIRouter(prefix="/payments", tags=["Payments"])


@payments_router.post(
    "/webhook",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def stripe_webhook(
    request: Request,
    payment_service: Annotated[StripePaymentService, FromComponent(ComponentEnum.PAYMENTS)],
) -> None:
    payload = await request.body()
    signature_header = request.headers.get("stripe-signature")
    return await payment_service.handle_webhook(payload=payload, signature_header=signature_header)


@payments_router.post(
    "/create-checkout-session",
    responses={
        status.HTTP_201_CREATED: {"model": CheckoutResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_checkout_session(
    request_data: CreateCheckoutRequest,
    payment_service: Annotated[StripePaymentService, FromComponent(ComponentEnum.PAYMENTS)],
    labour_service: Annotated[LabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CheckoutResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    labour = await labour_service.can_update_labour_payment_plan(
        requester_id=user.id, labour_id=request_data.labour_id, payment_plan=request_data.upgrade
    )

    item = ""
    if request_data.upgrade == "inner_circle":
        item = Product.UPGRADE_TO_INNER_CIRCLE.value
    elif request_data.upgrade == "community":
        if labour.payment_plan == "inner_circle":
            item = Product.UPGRADE_TO_COMMUNITY_FROM_INNER_CIRCLE.value
        else:
            item = Product.UPGRADE_TO_COMMUNITY.value

    checkout = await payment_service.create_checkout_session(
        user=user,
        success_url=request_data.success_url,
        cancel_url=request_data.cancel_url,
        item=item,
        labour_id=request_data.labour_id,
    )
    return CheckoutResponse(id=checkout.id, url=checkout.url)
