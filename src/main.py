"""FastAPI application factory and ASGI entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import dispose_engine
from src.health.router import router as health_router
from src.logging_config import RequestLoggingMiddleware, configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Wire process-level concerns: logging in, engine disposal out."""
    configure_logging()
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    """Build the application: JSON request logging, health router, docs always on."""
    app = FastAPI(
        title="User Management API",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(health_router)
    return app


app = create_app()
