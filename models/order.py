
from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    ForeignKey,
    DateTime,
    Sequence,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


# Order model
order_id_seq = Sequence("orders_id_seq")


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        order_id_seq,
        primary_key=True,
        server_default=order_id_seq.next_value(),
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    total = Column(Numeric(10, 2), nullable=False)

    status = Column(
        String(50),
        default="PLACED",
        nullable=False,
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    tracking = relationship(
        "OrderTracking",
        back_populates="order",
        cascade="all, delete-orphan",
    )


# Order item model
order_item_id_seq = Sequence("order_items_id_seq")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(
        Integer,
        order_item_id_seq,
        primary_key=True,
        server_default=order_item_id_seq.next_value(),
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    order = relationship(
        "Order",
        back_populates="items",
    )


# Order tracking model
order_tracking_id_seq = Sequence("order_tracking_id_seq")


class OrderTracking(Base):
    __tablename__ = "order_tracking"

    id = Column(
        Integer,
        order_tracking_id_seq,
        primary_key=True,
        server_default=order_tracking_id_seq.next_value(),
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
    )

    status = Column(String(50), nullable=False)

    message = Column(String(500), nullable=True)

    timestamp = Column(
        DateTime,
        server_default=func.current_timestamp(),
    )

    order = relationship(
        "Order",
        back_populates="tracking",
    )
