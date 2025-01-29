from sqlalchemy import Table, Column, Integer, String, Float
from database import metadata
from pydantic import BaseModel

# SQLAlchemy Table for Products
products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("description", String(300)),
    Column("price", Float),
    Column("category", String(50)),
)

# Pydantic Model for Products
class ProductIn(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductOut(ProductIn):
    id: int
