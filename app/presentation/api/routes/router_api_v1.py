from fastapi import APIRouter

from app.presentation.api.routes.auth import auth_router
from app.presentation.api.routes.birthing_person import birthing_person_router
from app.presentation.api.routes.healthcheck import healthcheck_router
from app.presentation.api.routes.labour import labour_router

api_v1_router = APIRouter(
    prefix="/api/v1",
)

api_v1_sub_routers = (
    auth_router,
    labour_router,
    birthing_person_router,
    healthcheck_router,
)

for router in api_v1_sub_routers:
    api_v1_router.include_router(router)
