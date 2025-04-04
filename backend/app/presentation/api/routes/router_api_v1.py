from fastapi import APIRouter

from app.labour.interfaces.api.routes.router import labour_module_router
from app.labour.interfaces.api.routes.subscription import subscription_router
from app.labour.interfaces.api.routes.subscription_management import subscription_management_router
from app.presentation.api.routes.auth import auth_router
from app.presentation.api.routes.contact import contact_us_router
from app.presentation.api.routes.healthcheck import healthcheck_router
from app.presentation.api.routes.payments import payments_router
from app.presentation.api.routes.subscriber import subscriber_router
from app.presentation.api.routes.twilio import twilio_router
from app.presentation.api.routes.user import user_router

api_v1_router = APIRouter(
    prefix="/api/v1",
)

api_v1_sub_routers = (
    auth_router,
    contact_us_router,
    user_router,
    labour_module_router,
    subscription_router,
    subscription_management_router,
    subscriber_router,
    payments_router,
    twilio_router,
    healthcheck_router,
)

for router in api_v1_sub_routers:
    api_v1_router.include_router(router)
