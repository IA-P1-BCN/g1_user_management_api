"""Schemas for the health endpoints."""

from pydantic import BaseModel


class HealthOut(BaseModel):
    """Liveness response."""

    status: str


class ReadyOut(BaseModel):
    """Readiness response; `dependency` names what is down on failure."""

    status: str
    dependency: str | None = None
