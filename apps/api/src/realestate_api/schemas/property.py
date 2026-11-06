from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PropertyCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    city: str = Field(min_length=2, max_length=100)
    price: Decimal = Field(gt=0, max_digits=14, decimal_places=2)


class PropertyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    city: str
    price: Decimal
    created_at: datetime
