"""Health endpoints: liveness without a database, readiness with a stubbed one."""

from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport

from src.database import get_db
from src.main import create_app


class StubSession:
    """Minimal AsyncSession stand-in for dependency-overridden tests."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.executed = False

    async def execute(self, *_args: Any, **_kwargs: Any) -> Any:
        self.executed = True
        if self.fail:
            raise RuntimeError("database is down")
        return None


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        yield http


async def test_health_returns_200_without_any_database(client: httpx.AsyncClient) -> None:
    """Liveness never touches the database, so it stays 200 even with no DB wired."""
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_ready_returns_200_when_database_answers(
    app: FastAPI, client: httpx.AsyncClient
) -> None:
    stub = StubSession()

    async def override() -> AsyncIterator[StubSession]:
        yield stub

    app.dependency_overrides[get_db] = override

    response = await client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "dependency": None}
    assert stub.executed


async def test_ready_returns_503_naming_the_down_dependency(
    app: FastAPI, client: httpx.AsyncClient
) -> None:
    async def override() -> AsyncIterator[StubSession]:
        yield StubSession(fail=True)

    app.dependency_overrides[get_db] = override

    response = await client.get("/ready")

    assert response.status_code == 503
    body = response.json()["detail"]
    assert body["dependency"] == "database"
    assert body["status"] == "unavailable"


async def test_swagger_ui_is_served(client: httpx.AsyncClient) -> None:
    response = await client.get("/docs")

    assert response.status_code == 200
    assert b"swagger" in response.content.lower()


async def test_redoc_is_served(client: httpx.AsyncClient) -> None:
    response = await client.get("/redoc")

    assert response.status_code == 200
    assert b"redoc" in response.content.lower()
