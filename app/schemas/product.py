from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    active_users: int | None = Field(default=None, ge=0)

    selling: bool = False
    seaking_inversion: bool = False
    publish: bool = False

    price: float | None = Field(default=None, ge=0)

    founder_id: int | None = Field(default=None, ge=1)

    is_company: bool = False
    country: str | None = Field(default=None, max_length=100)
    launch_date: datetime | None = None
    publish_date: datetime | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    active_users: int | None = Field(default=None, ge=0)

    selling: bool | None = None
    seaking_inversion: bool | None = None
    publish: bool | None = None

    price: float | None = Field(default=None, ge=0)

    founder_id: int | None = Field(default=None, ge=1)

    is_company: bool | None = None
    country: str | None = Field(default=None, max_length=100)
    launch_date: datetime | None = None
    publish_date: datetime | None = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

