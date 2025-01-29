from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Product model
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

# In-memory product database
products: List[Product] = []

@app.get("/")
def root():
    return {"message": "Welcome to the Product Management API"}

@app.get("/products/", response_model=List[Product])
def get_products():
    """Retrieve all products."""
    return products

@app.post("/products/", status_code=201)
def create_product(product: Product):
    """Add a new product."""
    if any(p.id == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product ID already exists.")
    products.append(product)
    return {"message": "Product added successfully!"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Delete a product by ID."""
    global products
    products = [p for p in products if p.id != product_id]
    return {"message": "Product deleted successfully"}
