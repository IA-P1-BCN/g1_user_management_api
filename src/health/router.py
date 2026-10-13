"""Liveness (`/health`) and readiness (`/ready`) endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.health.schemas import HealthOut, ReadyOut

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthOut)
async def health() -> HealthOut:
    """Liveness: the process is up. Never checks the database."""
    return HealthOut(status="ok")


@router.get("/ready", response_model=ReadyOut)
async def ready(session: Annotated[AsyncSession, Depends(get_db)]) -> ReadyOut:
    """Readiness: verify the database connection before serving traffic."""
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "unavailable", "dependency": "database"},
        ) from exc
    return ReadyOut(status="ready")
