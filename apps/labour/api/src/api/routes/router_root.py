from typing import Annotated, Any

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse

from src.api.routes.router_api_v1 import api_v1_router
from src.setup.settings import Settings

root_router = APIRouter()


@root_router.get("/", tags=["General"])
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="docs")


@root_router.get("/docs", tags=["General"])
@inject
async def docs(settings: Annotated[Settings, FromComponent()]) -> HTMLResponse:
    if settings.base.environment != "production":
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    return HTMLResponse(content="Forbidden", status_code=403)


@root_router.get("/openapi.json", tags=["General"])
@inject
async def openapi(settings: Annotated[Settings, FromComponent()]) -> dict[str, Any]:
    if settings.base.environment != "production":
        return get_openapi(title="Labour Tracker", version="0.1.0", routes=root_router.routes)
    return {"status": "Forbidden"}


@root_router.get("/redoc", tags=["General"])
@inject
async def redoc(settings: Annotated[Settings, FromComponent()]) -> HTMLResponse:
    if settings.base.environment != "production":
        return get_redoc_html(openapi_url="/openapi.json", title="docs")
    return HTMLResponse(content="Forbidden", status_code=403)


root_sub_routers = (api_v1_router,)

for router in root_sub_routers:
    root_router.include_router(router)
