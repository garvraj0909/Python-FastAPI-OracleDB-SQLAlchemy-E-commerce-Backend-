from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session, selectinload

from models.user import User
from models.product import Product
from models.order import Order, OrderItem, OrderTracking


class OrderService:

    # CREATE ORDER
    def create_order(
        self,
        db: Session,
        user_id: int,
        items
    ):

        # Check if user exists
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            return None, "User not found"

        order_items = []
        total = Decimal("0.00")

        # Check products and stock
        for item in items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            if product is None:
                return None, (
                    f"Product {item.product_id} not found"
                )

            if item.quantity <= 0:
                return None, "Quantity must be greater than 0"

            if product.stock < item.quantity:
                return None, (
                    f"Not enough stock for {product.name}"
                )

            item_price = product.price * item.quantity

            total += item_price

            # Create OrderItem object
            order_item = OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )

            order_items.append(order_item)

        # Reduce stock
        for item in items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            product.stock -= item.quantity

        # Create order
        order = Order(
            user_id=user_id,
            total=total,
            status="PLACED"
        )

        # Add order items
        order.items = order_items

        # Initial tracking event
        tracking = OrderTracking(
            status="PLACED",
            message="Order has been placed",
            timestamp=datetime.now()
        )

        order.tracking.append(tracking)

        # Save everything
        db.add(order)
        db.commit()
        db.refresh(order)

        return order, None

    # GET ALL ORDERS
    def get_orders(self, db: Session):

        return (
            db.query(Order)
            .options(
                selectinload(Order.items)
            )
            .all()
        )

    # GET ONE ORDER
    def get_order(
        self,
        db: Session,
        order_id: int
    ):

        return (
            db.query(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.tracking)
            )
            .filter(Order.id == order_id)
            .first()
        )

    # UPDATE ORDER STATUS
    def update_order_status(
        self,
        db: Session,
        order_id: int,
        status: str
    ):

        order = self.get_order(
            db,
            order_id
        )

        if order is None:
            return None, "Order not found"

        allowed_statuses = [
            "PLACED",
            "CONFIRMED",
            "SHIPPED",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "CANCELLED"
        ]

        status = status.upper()

        if status not in allowed_statuses:
            return None, (
                "Invalid status. Allowed statuses are: "
                "PLACED, CONFIRMED, SHIPPED, "
                "OUT_FOR_DELIVERY, DELIVERED, CANCELLED"
            )

        # Don't add duplicate status
        if order.status == status:
            return None, "Order already has this status"

        # Update current status
        order.status = status

        # Status messages
        messages = {
            "PLACED": "Order has been placed",
            "CONFIRMED": "Order has been confirmed",
            "SHIPPED": "Order has been shipped",
            "OUT_FOR_DELIVERY": "Order is out for delivery",
            "DELIVERED": "Order has been delivered",
            "CANCELLED": "Order has been cancelled"
        }

        # Create tracking event
        tracking_event = OrderTracking(
            status=status,
            message=messages[status],
            timestamp=datetime.now()
        )

        order.tracking.append(tracking_event)

        db.commit()
        db.refresh(order)

        return order, None

    # GET ORDER TRACKING
    def get_order_tracking(
        self,
        db: Session,
        order_id: int
    ):

        order = self.get_order(
            db,
            order_id
        )

        if order is None:
            return None

        return {
            "order_id": order.id,
            "current_status": order.status,
            "tracking": order.tracking
        }

    # DELETE ORDER
    def delete_order(
        self,
        db: Session,
        order_id: int
    ):

        order = self.get_order(
            db,
            order_id
        )

        if order is None:
            return False

        db.delete(order)
        db.commit()

        return True