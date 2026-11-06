from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from realestate_api.core.database import get_db
from realestate_api.schemas.property import PropertyCreate, PropertyOut
from realestate_api.services import property_service

router = APIRouter(prefix="/properties", tags=["properties"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("", response_model=PropertyOut, status_code=201)
async def create_property(data: PropertyCreate, db: DbSession) -> PropertyOut:
    return await property_service.create_property(db, data)


@router.get("", response_model=list[PropertyOut])
async def list_properties(
    db: DbSession,
    city: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[PropertyOut]:
    return await property_service.list_properties(db, city, limit, offset)
