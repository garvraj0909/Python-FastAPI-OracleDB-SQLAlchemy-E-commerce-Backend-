
from sqlalchemy import Column, Integer, String, Numeric, Sequence
from database.database import Base


product_id_seq = Sequence("products_id_seq")


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        product_id_seq,
        primary_key=True,
        server_default=product_id_seq.next_value()
    )
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
