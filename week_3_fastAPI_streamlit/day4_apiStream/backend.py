from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from starlette.middleware.gzip import GZipMiddleware
from aiocache import cached
from multiprocessing import Pool
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import asyncio

# Constants for JWT
SECRET_KEY = "your_secret_key"  # Replace with a strong key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI Initialization
app = FastAPI(
    title="High-Performance FastAPI Application",
    description="An optimized FastAPI app with async calls, caching, database, and CPU-bound task handling.",
    version="1.0.0",
)

# Middleware for Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# OAuth2 and Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

# Fake Databases
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": pwd_context.hash("testpassword"),
        "disabled": False,
    }
}

products = [
    {"id": i, "name": f"Product {i}", "description": f"Description {i}", "price": i * 10.0}
    for i in range(1, 101)
]

# Helper Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str) -> Optional[UserInDB]:
    user = fake_users_db.get(username)
    if user:
        return UserInDB(**user)
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Multiprocessing Example for CPU-bound Tasks
def compute_task(n: int) -> int:
    return sum(i ** 2 for i in range(n))

# Caching Example for Expensive Operations
@cached(ttl=60)
async def expensive_operation():
    await asyncio.sleep(2)  # Simulate long computation
    return {"message": "Cached Response"}

# Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to the High-Performance FastAPI App!",
        "docs": "/docs",
        "redoc": "/redoc",
    }

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/products/", dependencies=[Depends(oauth2_scheme)])
async def get_products(skip: int = 0, limit: int = 10):
    """Retrieve paginated products."""
    return products[skip: skip + limit]

@app.post("/products/", dependencies=[Depends(oauth2_scheme)])
async def create_product(product: Product):
    """Add a new product."""
    if any(p["id"] == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product ID already exists.")
    products.append(product.dict())
    return {"message": "Product added successfully!", "product": product}

@app.get("/cached-operation", dependencies=[Depends(oauth2_scheme)])
async def cached_operation():
    """Simulates a long operation with caching."""
    return await expensive_operation()

@app.get("/optimized-cpu/", dependencies=[Depends(oauth2_scheme)])
def optimized_cpu_task():
    """Handle CPU-bound tasks using multiprocessing."""
    with Pool(processes=4) as pool:  # Use 4 worker processes
        result = pool.map(compute_task, [10_000_000])
    return {"result": result}

@app.delete("/products/{product_id}", dependencies=[Depends(oauth2_scheme)])
async def delete_product(product_id: int):
    """Delete a product by ID."""
    global products
    products = [p for p in products if p["id"] != product_id]
    return {"message": "Product deleted successfully"}

# Async I/O Endpoint
@app.get("/async-io", dependencies=[Depends(oauth2_scheme)])
async def async_io_operation():
    """Handle non-blocking I/O."""
    await asyncio.sleep(2)  # Simulate I/O operation
    return {"message": "Completed Async I/O Operation"}
