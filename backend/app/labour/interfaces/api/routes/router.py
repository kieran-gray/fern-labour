from fastapi import APIRouter

from app.labour.interfaces.api.routes.contraction import contraction_router
from app.labour.interfaces.api.routes.labour import labour_router
from app.labour.interfaces.api.routes.labour_update import labour_update_router
from app.labour.interfaces.api.routes.subscription import subscription_router
from app.labour.interfaces.api.routes.subscription_management import subscription_management_router

labour_module_router = APIRouter()

labour_sub_routers = (
    contraction_router,
    labour_update_router,
)

for router in labour_sub_routers:
    labour_router.include_router(router)

module_sub_routers = (labour_router, subscription_router, subscription_management_router)

for router in module_sub_routers:
    labour_module_router.include_router(router)
