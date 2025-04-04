from fastapi import APIRouter

from app.labour.interfaces.api.routes.contraction import contraction_router
from app.labour.interfaces.api.routes.labour import labour_router
from app.labour.interfaces.api.routes.labour_update import labour_update_router

labour_module_router = APIRouter(
    prefix="/labour",
)

# Omitting subscription and subscription_management for backwards compatibility
labour_sub_routers = (
    labour_router,
    labour_update_router,
    contraction_router,
)

for router in labour_sub_routers:
    labour_module_router.include_router(router)
