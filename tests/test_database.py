"""Database wiring: get_db yields a session from the factory and closes it."""

from collections.abc import AsyncIterator
from typing import Any

import pytest

from src.database import get_db


class StubSession:
    def __init__(self) -> None:
        self.closed = False


class StubSessionContextManager:
    def __init__(self, session: StubSession) -> None:
        self._session = session

    async def __aenter__(self) -> StubSession:
        return self._session

    async def __aexit__(self, *_exc: Any) -> bool:
        self._session.closed = True
        return False


def stub_factory(monkeypatch: pytest.MonkeyPatch) -> StubSession:
    session = StubSession()
    monkeypatch.setattr(
        "src.database.get_session_factory",
        lambda: lambda: StubSessionContextManager(session),
    )
    return session


async def test_get_db_yields_the_factory_session(monkeypatch: pytest.MonkeyPatch) -> None:
    session = stub_factory(monkeypatch)

    yielded: list[StubSession] = []
    async for db in get_db():
        yielded.append(db)

    assert yielded == [session]


async def test_get_db_closes_the_session_when_the_request_ends(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = stub_factory(monkeypatch)

    async for _db in get_db():
        pass

    assert session.closed is True
