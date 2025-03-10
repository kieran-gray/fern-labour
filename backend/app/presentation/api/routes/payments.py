from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials

from app.infrastructure.auth.interfaces.controller import AuthController
from app.infrastructure.payments.stripe.stripe_payment_service import StripePaymentService
from app.presentation.api.dependencies import bearer_scheme
from app.presentation.api.schemas.requests.payments import CreateCheckoutRequest
from app.presentation.api.schemas.responses.payments import CheckoutResponse
from app.presentation.exception_handler import ExceptionSchema
from app.setup.ioc.di_component_enum import ComponentEnum

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
async def my_webhook_view(
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
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CheckoutResponse:
    # TODO check labour payment plan
    user = auth_controller.get_authenticated_user(credentials=credentials)
    checkout = await payment_service.create_checkout_session(
        user=user,
        success_url=request_data.success_url,
        cancel_url=request_data.cancel_url,
        item=request_data.upgrade,
        labour_id=request_data.labour_id,
    )
    return CheckoutResponse(id=checkout.id, url=checkout.url)
