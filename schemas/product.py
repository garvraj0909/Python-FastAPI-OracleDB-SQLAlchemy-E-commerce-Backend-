from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)