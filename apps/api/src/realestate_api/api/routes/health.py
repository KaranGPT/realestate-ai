from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from realestate_api.core.config import get_settings
from realestate_api.core.database import get_db
from realestate_api.schemas.health import DbHealthResponse, HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", environment=settings.environment)


@router.get("/health/db", response_model=DbHealthResponse)
async def health_db(db: Annotated[AsyncSession, Depends(get_db)]) -> DbHealthResponse:
    try:
        await db.execute(text("SELECT 1"))
    except (SQLAlchemyError, OSError) as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return DbHealthResponse(status="ok", database="up")
