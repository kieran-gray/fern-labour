from fastapi import APIRouter

from src.subscription.api.routes.subscriber import subscriber_router
from src.subscription.api.routes.subscription import subscription_router
from src.subscription.api.routes.subscription_management import (
    subscription_management_router,
)

subscription_module_router = APIRouter()

module_sub_routers = (
    subscription_router,
    subscription_management_router,
    subscriber_router,
)

for router in module_sub_routers:
    subscription_module_router.include_router(router)
