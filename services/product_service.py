from sqlalchemy.orm import Session

from models.product import Product


class ProductService:

    def create_product(
        self,
        db: Session,
        name: str,
        description: str,
        price: float,
        stock: int
    ):

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    def get_products(self, db: Session):

        return db.query(Product).all()

    def get_product(
        self,
        db: Session,
        product_id: int
    ):

        return db.query(Product).filter(
            Product.id == product_id
        ).first()

    def update_product(
        self,
        db: Session,
        product_id: int,
        name: str,
        description: str,
        price: float,
        stock: int
    ):

        product = self.get_product(
            db,
            product_id
        )

        if product is None:
            return None

        product.name = name
        product.description = description
        product.price = price
        product.stock = stock

        db.commit()
        db.refresh(product)

        return product

    def delete_product(
        self,
        db: Session,
        product_id: int
    ):

        product = self.get_product(
            db,
            product_id
        )

        if product is None:
            return False

        db.delete(product)
        db.commit()

        return True