from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory storage for products
products = []

# Pydantic model for Product
class Product(BaseModel):
    name: str
    description: str
    picLink: str
    category: str

# Root route
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the FastAPI application!"}

# Favicon route
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """
    Endpoint to handle favicon requests.
    """
    return {"message": "Favicon not available"}

# POST Endpoint: Add a new product
@app.post("/products/")
def add_product(product: Product):
    """
    Add a new product to the in-memory storage.

    Args:
        product (Product): The product data provided in the request body.

    Returns:
        dict: A message confirming the addition of the product.
    """
    product_data = product.dict()  # Convert Pydantic model to dictionary
    products.append(product_data)
    return {"message": "Product added successfully!", "product": product_data}

# GET Endpoint: Retrieve all products
@app.get("/products/")
def get_all_products(category: Optional[str] = None):
    """
    Retrieve all stored products or filter by category.

    Args:
        category (str, optional): The category to filter products by.

    Returns:
        list: A list of all products or filtered products.
    """
    if category:
        filtered_products = [product for product in products if product["category"] == category]
        return filtered_products
    return products

# GET Endpoint: Retrieve product by ID
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The ID of the product.

    Returns:
        dict: Product details if found, or an error message if not found.
    """
    if product_id < 1 or product_id > len(products):
        return {"error": "Product not found"}
    return products[product_id - 1]
