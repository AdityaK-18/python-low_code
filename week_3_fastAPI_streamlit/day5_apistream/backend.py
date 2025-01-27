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

# In-memory database
products = []

# Create a product
@app.post("/products/")
def create_product(product: Product):
    if any(p["id"] == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product ID already exists.")
    products.append(product.dict())
    return product

# Bulk upload products
@app.post("/products/bulk/")
def bulk_upload_products(new_products: List[Product]):
    for product in new_products:
        if any(p["id"] == product.id for p in products):
            raise HTTPException(status_code=400, detail=f"Product ID {product.id} already exists.")
        products.append(product.dict())
    return {"message": f"{len(new_products)} products added successfully!"}

# Get all products
@app.get("/products/")
def get_products():
    return products

# Update a product
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for product in products:
        if product["id"] == product_id:
            product.update(updated_product.dict())
            return product
    raise HTTPException(status_code=404, detail="Product not found.")

# Delete a product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    global products
    products = [p for p in products if p["id"] != product_id]
    return {"message": "Product deleted successfully"}
