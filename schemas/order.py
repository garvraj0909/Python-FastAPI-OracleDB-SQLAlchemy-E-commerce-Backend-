from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(
        from_attributes=True
    )


class TrackingUpdate(BaseModel):
    status: str


class TrackingResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: list[OrderItemResponse]
    total: float
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )


class OrderTrackingResponse(BaseModel):
    order_id: int
    current_status: str
    tracking: list[TrackingResponse]

    model_config = ConfigDict(
        from_attributes=True
    )