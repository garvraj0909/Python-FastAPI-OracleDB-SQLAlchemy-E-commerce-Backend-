from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderTrackingResponse(BaseModel):
    id: int
    status: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TrackingUpdate(BaseModel):
    status: str = Field(min_length=1)
    description: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: Decimal
    status: str
    items: list[OrderItemResponse] = Field(default_factory=list)
    tracking: list[OrderTrackingResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
