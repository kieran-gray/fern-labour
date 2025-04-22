from fastapi import APIRouter

from src.labour.presentation.api.routes.contraction import contraction_router
from src.labour.presentation.api.routes.labour import labour_router
from src.labour.presentation.api.routes.labour_query import labour_query_router
from src.labour.presentation.api.routes.labour_update import labour_update_router
from src.subscription.presentation.api.routes.subscription import subscription_router
from src.subscription.presentation.api.routes.subscription_management import (
    subscription_management_router,
)

labour_module_router = APIRouter()

module_sub_routers = (
    labour_router,
    contraction_router,
    labour_update_router,
    labour_query_router,
    subscription_router,
    subscription_management_router,
)

for router in module_sub_routers:
    labour_module_router.include_router(router)
