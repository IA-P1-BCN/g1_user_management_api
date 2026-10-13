"""Async engine and session factory: one engine per process, created lazily."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import get_settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Create the process-wide async engine on first use (connection stays lazy)."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(str(get_settings().database_url), pool_pre_ping=True)
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the session factory bound to the process engine."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _session_factory


async def get_db() -> AsyncIterator[AsyncSession]:
    """Yield a request-scoped session; the context manager closes it afterwards."""
    async with get_session_factory()() as session:
        yield session


async def dispose_engine() -> None:
    """Dispose the engine on application shutdown."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
