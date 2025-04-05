from typing import Annotated, Any

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials

from app.api.dependencies import bearer_scheme
from app.api.routes.router_api_v1 import api_v1_router
from app.user.infrastructure.auth.interfaces.controller import AuthController

root_router = APIRouter()


@root_router.get("/", tags=["General"])
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="docs")


@root_router.get("/docs", tags=["General"])
@inject
async def docs(
    auth_controller: Annotated[AuthController, FromComponent()],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> HTMLResponse:
    _ = auth_controller.get_authenticated_user(credentials)
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@root_router.get("/openapi.json", tags=["General"])
@inject
async def openapi(
    auth_controller: Annotated[AuthController, FromComponent()],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict[str, Any]:
    _ = auth_controller.get_authenticated_user(credentials)
    return get_openapi(title="Labour Tracker", version="0.1.0", routes=root_router.routes)


@root_router.get("/redoc", tags=["General"])
@inject
async def redoc(
    auth_controller: Annotated[AuthController, FromComponent()],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> HTMLResponse:
    _ = auth_controller.get_authenticated_user(credentials)
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


root_sub_routers = (api_v1_router,)

for router in root_sub_routers:
    root_router.include_router(router)
