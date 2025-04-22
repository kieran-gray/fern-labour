from fastapi import APIRouter

from src.admin.presentation.api.routes.contact import contact_us_router
from src.api.routes.healthcheck import healthcheck_router
from src.labour.presentation.api.routes.router import labour_module_router
from src.payments.presentation.api.routes.payments import payments_router
from src.subscription.presentation.api.routes.router import subscription_module_router
from src.user.presentation.api.routes.auth import auth_router
from src.user.presentation.api.routes.user import user_router

api_v1_router = APIRouter(
    prefix="/api/v1",
)

api_v1_sub_routers = (
    auth_router,
    contact_us_router,
    user_router,
    labour_module_router,
    subscription_module_router,
    payments_router,
    healthcheck_router,
)

for router in api_v1_sub_routers:
    api_v1_router.include_router(router)
