from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Root route to fix "Not Found" error
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the FastAPI Application!"}

# Example: Path parameter route
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    """
    Retrieve product details by its ID.

    Args:
        product_id (int): The ID of the product.

    Returns:
        dict: Product details if found, or an error message.
    """
    sample_products = {
        1: {"name": "Milk", "category": "grocery", "price": 2.5},
        2: {"name": "Laptop", "category": "electronics", "price": 1000},
    }
    product = sample_products.get(product_id)
    if product:
        return product
    return {"error": "Product not found"}

# Example: Query parameter route
@app.get("/products/")
def get_products_by_category(category: Optional[str] = None):
    """
    Retrieve products filtered by category.

    Args:
        category (str, optional): The category to filter products by.

    Returns:
        list: Filtered list of products or all products.
    """
    sample_products = [
        {"id": 1, "name": "Milk", "category": "grocery", "price": 2.5},
        {"id": 2, "name": "Laptop", "category": "electronics", "price": 1000},
        {"id": 3, "name": "Bread", "category": "grocery", "price": 1.5},
    ]
    if category:
        filtered_products = [product for product in sample_products if product["category"] == category]
        return filtered_products
    return sample_products
