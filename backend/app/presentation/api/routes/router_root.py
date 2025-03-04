from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.presentation.api.routes.router_api_v1 import api_v1_router

root_router = APIRouter()


@root_router.get("/", tags=["General"])
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="docs")


# @root_router.get("/docs", tags=["General"])
# @inject
# async def docs(
#     auth_controller: Annotated[AuthController, FromComponent()],
#     credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
# ) -> HTMLResponse:
#     _ = auth_controller.get_authenticated_user(credentials)
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


# @root_router.get("/openapi.json", tags=["General"])
# @inject
# async def openapi(
#     auth_controller: Annotated[AuthController, FromComponent()],
#     credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
# ) -> dict[str, Any]:
#     _ = auth_controller.get_authenticated_user(credentials)
#     return get_openapi(title="Labour Tracker", version="0.1.0", routes=root_router.routes)


# @root_router.get("/redoc", tags=["General"])
# @inject
# async def redoc(
#     auth_controller: Annotated[AuthController, FromComponent()],
#     credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
# ) -> HTMLResponse:
#     _ = auth_controller.get_authenticated_user(credentials)
#     return get_redoc_html(openapi_url="/openapi.json", title="docs")


root_sub_routers = (api_v1_router,)

for router in root_sub_routers:
    root_router.include_router(router)
