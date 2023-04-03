"""The main module"""

from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from functools import (
    lru_cache,
)
from typing import (
    Dict,
)
import uvicorn

from app.config import (
    settings,
)
from app.models import (
    router as models_router,
)


@lru_cache()
def get_app() -> FastAPI:
    """
    A method that creates, configures and returns a FastAPI app instance

    Return:
        FastAPI : a FastAPI app instance
    """
    app_settings = settings()
    if app_settings.DEBUG == "info":
        app = FastAPI(
            docs_url="/docs",
            redoc_url="/redocs",
            title="Truth Guard Server",
            description="The server side of Truth Guard.",
            version="1.0",
            openapi_url="/api/v1/openapi.json",
        )
    else:
        app = FastAPI(
            docs_url=None,
            redoc_url=None,
            title=None,
            description=None,
            version=None,
            openapi_url=None,
        )
    app = FastAPI(
        docs_url="/docs",
        redoc_url="/redocs",
        title="Truth Guard",
        description="The server side of Truth Guard.",
        version="0.1.0",
        openapi_url="/api/v1/openapi.json",
    )

    origins = [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://localhost:3000",
    ]

    origins.extend(app_settings.cors_origins)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api")
    async def root() -> Dict[str, str]:
        return {"message": "Welcome to Truth Guard Server."}

    app.include_router(models_router.router, tags=["models"])

    return app


fake_news_app = get_app()


def serve() -> None:
    """
    A method that run a uvicorn command.
    """
    try:
        uvicorn.run(
            "app.main:fake_news_app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
    except Exception:
        ...


if __name__ == "__main__":
    serve()
