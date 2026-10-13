
from fastapi import FastAPI

#from database.database import engine, Base

from models import (
    User,
    Product,
    Order,
    OrderItem,
    OrderTracking
)

from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.products import router as products_router
from routers.orders import router as orders_router


app = FastAPI(
    title="E-Commerce Backend APIs",
    description="E-Commerce backend using FastAPI, OracleDB and PostgreSQL and SQLAlchemy",
    version="1.0.0"
)

#Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "message": "E-Commerce Backend APIs are running"
    }
