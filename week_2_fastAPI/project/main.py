from fastapi import FastAPI, HTTPException
from database import database, metadata, engine
from models import products, ProductIn, ProductOut

app = FastAPI()

# Create database tables
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Product Management API"}


# Get All Products
@app.get("/products/", response_model=list[ProductOut])
async def get_all_products():
    query = products.select()
    return await database.fetch_all(query)


# Get Product by ID
@app.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Add New Product
@app.post("/products/", response_model=ProductOut)
async def create_product(product: ProductIn):
    query = products.insert().values(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
    )
    product_id = await database.execute(query)
    return {**product.dict(), "id": product_id}


# Update Product
@app.put("/products/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
    )
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {**product.dict(), "id": product_id}


# Delete Product
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product with ID {product_id} deleted successfully"}
