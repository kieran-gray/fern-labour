from fastapi import APIRouter

from src.api.routes.healthcheck import healthcheck_router
from src.notification.presentation.api.routes.twilio import twilio_router
from src.user.presentation.api.routes.auth import auth_router
from src.user.presentation.api.routes.user import user_router

api_v1_router = APIRouter(
    prefix="/api/v1",
)

api_v1_sub_routers = (
    auth_router,
    user_router,
    twilio_router,
    healthcheck_router,
)

for router in api_v1_sub_routers:
    api_v1_router.include_router(router)
