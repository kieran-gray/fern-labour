from fastapi import APIRouter
from fastapi.requests import Request

healthcheck_router = APIRouter()


@healthcheck_router.get("/health", tags=["Health"])
async def healthcheck(_: Request) -> dict[str, str]:
    return {"status": "ok"}
