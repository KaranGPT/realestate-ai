from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from realestate_api.models.property import Property
from realestate_api.schemas.property import PropertyCreate, PropertyUpdate


async def create_property(db: AsyncSession, data: PropertyCreate) -> Property:
    prop = Property(**data.model_dump())
    db.add(prop)
    await db.commit()
    await db.refresh(prop)
    return prop


async def list_properties(
    db: AsyncSession, city: str | None = None, limit: int = 20, offset: int = 0
) -> list[Property]:
    stmt = select(Property).order_by(Property.id).limit(limit).offset(offset)
    if city:
        stmt = stmt.where(Property.city.ilike(city))
    result = await db.scalars(stmt)
    return list(result)


async def get_property(db: AsyncSession, property_id: int) -> Property | None:
    return await db.get(Property, property_id)


async def update_property(db: AsyncSession, prop: Property, data: PropertyUpdate) -> Property:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)
    await db.commit()
    await db.refresh(prop)
    return prop


async def delete_property(db: AsyncSession, prop: Property) -> None:
    await db.delete(prop)
    await db.commit()
