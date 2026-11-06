from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from realestate_api.core.database import get_db
from realestate_api.models.property import Property
from realestate_api.schemas.property import PropertyCreate, PropertyOut, PropertyUpdate
from realestate_api.services import property_service

router = APIRouter(prefix="/properties", tags=["properties"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_property_or_404(property_id: int, db: DbSession) -> Property:
    prop = await property_service.get_property(db, property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


PropertyDep = Annotated[Property, Depends(get_property_or_404)]


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


@router.get("/{property_id}", response_model=PropertyOut)
async def get_property(prop: PropertyDep) -> PropertyOut:
    return prop


@router.patch("/{property_id}", response_model=PropertyOut)
async def update_property(data: PropertyUpdate, prop: PropertyDep, db: DbSession) -> PropertyOut:
    return await property_service.update_property(db, prop, data)


@router.delete("/{property_id}", status_code=204)
async def delete_property(prop: PropertyDep, db: DbSession) -> None:
    await property_service.delete_property(db, prop)
