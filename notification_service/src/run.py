from fastapi import FastAPI

from src.setup.app_factory import create_app_with_container
from src.setup.logs import configure_logging
from src.setup.settings import Settings

settings: Settings = Settings.from_file()
configure_logging(level=settings.logging.level)
app: FastAPI = create_app_with_container(settings)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.run:app",
        host=settings.uvicorn.host,
        port=settings.uvicorn.port,
        reload=settings.uvicorn.reload,
        loop="uvloop",
    )
