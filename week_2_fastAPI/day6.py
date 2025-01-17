from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Simulated database for products
products_db = {
    1: {
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 1200.50,
        "category": "Electronics",
    },
    2: {
        "name": "Chair",
        "description": "Comfortable office chair",
        "price": 150.00,
        "category": "Furniture",
    },
}


# Pydantic model for Product
class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Smartphone")
    description: str = Field(
        ...,
        min_length=10,
        max_length=300,
        example="A high-end smartphone with excellent features",
    )
    price: float = Field(..., gt=0, example=999.99)
    category: str = Field(..., min_length=3, max_length=50, example="Electronics")


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint to verify the application is running.
    """
    return {"message": "Welcome to the FastAPI application!"}


# List all products
@app.get("/products/")
async def list_products(category: Optional[str] = Query(None, example="Electronics")):
    """
    List all products or filter them by category.
    """
    if category:
        filtered_products = {
            id: prod
            for id, prod in products_db.items()
            if prod["category"].lower() == category.lower()
        }
        if not filtered_products:
            raise HTTPException(
                status_code=404, detail=f"No products found in category '{category}'"
            )
        return {"products": filtered_products}
    return {"products": products_db}


# Get product by ID
@app.get("/products/{product_id}")
async def get_product(product_id: int = Path(..., gt=0, example=1)):
    """
    Fetch a product by its ID.
    """
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found"
        )
    return {"product": product}


# Create a new product
@app.post("/products/")
async def create_product(product: Product):
    """
    Add a new product to the database.
    """
    # Check for duplicate product name
    if any(
        prod["name"].lower() == product.name.lower() for prod in products_db.values()
    ):
        raise HTTPException(
            status_code=400, detail=f"Product with name '{product.name}' already exists"
        )

    new_id = max(products_db.keys()) + 1 if products_db else 1
    products_db[new_id] = product.dict()
    return {"message": "Product created successfully", "product_id": new_id}


# Update an existing product
@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    """
    Update an existing product by ID.
    """
    if product_id not in products_db:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found"
        )

    # Update the product details
    products_db[product_id] = product.dict()
    return {
        "message": f"Product with ID {product_id} updated successfully",
        "product": product,
    }


# Delete a product by ID
@app.delete("/products/{product_id}")
async def delete_product(product_id: int = Path(..., gt=0, example=1)):
    """
    Delete a product by its ID.
    """
    if product_id not in products_db:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found"
        )
    del products_db[product_id]
    return {"message": f"Product with ID {product_id} deleted successfully"}


# Custom validation error handler
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    """
    Handles all uncaught exceptions and provides a custom error message.
    """
    return {"error": "An unexpected error occurred", "details": str(exc)}
