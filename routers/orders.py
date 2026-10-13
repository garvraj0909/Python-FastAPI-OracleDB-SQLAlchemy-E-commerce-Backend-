from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.security import get_current_user

from schemas.order import (
    OrderCreate,
    OrderResponse,
    TrackingUpdate,
    OrderTrackingResponse
)

from services.order_service import OrderService
from database.database import get_db


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_user)]
)


order_service = OrderService()


# CREATE ORDER
@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_order, error = order_service.create_order(
        db,
        current_user.id,
        order.items
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return new_order


# GET ALL ORDERS
@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db)
):

    return order_service.get_orders(db)


# GET ONE ORDER
@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = order_service.get_order(
        db,
        order_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# UPDATE ORDER STATUS
@router.put(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    tracking: TrackingUpdate,
    db: Session = Depends(get_db)
):

    order, error = order_service.update_order_status(
        db,
        order_id,
        tracking.status
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return order


# GET ORDER TRACKING
@router.get(
    "/{order_id}/tracking",
    response_model=OrderTrackingResponse
)
def get_order_tracking(
    order_id: int,
    db: Session = Depends(get_db)
):

    tracking = order_service.get_order_tracking(
        db,
        order_id
    )

    if tracking is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return tracking


# DELETE ORDER
@router.delete(
    "/{order_id}"
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    deleted = order_service.delete_order(
        db,
        order_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "message": "Order deleted successfully"
    }