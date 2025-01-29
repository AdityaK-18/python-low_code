from fastapi import FastAPI, Depends, HTTPException
from typing import Generator
import logging

app = FastAPI()

# Simulated Database
users_db = {
    "alice": {"username": "alice", "role": "admin"},
    "bob": {"username": "bob", "role": "user"},
    "aditya": {"username": "aditya", "role": "admin"},
    "Apporv": {"username": "Apporv", "role": "admin"},
    "Manoj": {"username": "Manoj", "role": "admin"}
}

# Dependency: Simulating a database connection
def get_database() -> Generator:
    """
    Simulates a database connection.
    Yields a mocked database connection object.
    """
    db = {"connection": "Database connected", "users": users_db}
    try:
        yield db  # Resource is active here
    finally:
        db["connection"] = "Database disconnected"

# Dependency: Logger
def get_logger() -> logging.Logger:
    """
    Provides a logger instance.
    """
    logger = logging.getLogger("app-logger")
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

# Endpoint: Root
@app.get("/")
async def root(logger: logging.Logger = Depends(get_logger)):
    """
    Root endpoint to confirm the API is running.
    Injects a logger to log the access.
    """
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the FastAPI Dependency Injection Example!"}

# Endpoint: Database Status
@app.get("/db-status/")
async def db_status(db: dict = Depends(get_database), logger: logging.Logger = Depends(get_logger)):
    """
    Simulates checking the database status.
    Injects a database connection and a logger.
    """
    logger.info(f"Database status checked: {db['connection']}")
    return {"db_status": db["connection"]}

# Endpoint: Simulated Task
@app.get("/simulate-task/")
async def simulate_task(duration: int = 2, db: dict = Depends(get_database), logger: logging.Logger = Depends(get_logger)):
    """
    Simulates a task that requires a database connection and logging.
    Args:
        duration (int): The duration of the simulated task in seconds (default is 2).
    """
    logger.info(f"Simulated task started. Task duration: {duration} seconds.")
    logger.info(f"Database status: {db['connection']}")
    return {"message": f"Task completed in {duration} seconds", "db_status": db["connection"]}

# Endpoint: User Info
@app.get("/users/{username}/info")
async def get_user_info(username: str, db: dict = Depends(get_database), logger: logging.Logger = Depends(get_logger)):
    """
    Fetches and logs information about a user.
    Args:
        username (str): Username to fetch information for.
    """
    user = db["users"].get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User info requested for username: {username}")
    return {"user": user}

# Endpoint: Public User Creation
@app.post("/users/")
async def create_user(username: str, role: str = "user", db: dict = Depends(get_database), logger: logging.Logger = Depends(get_logger)):
    """
    Allows creating a new user in the database.
    Args:
        username (str): The username of the new user.
        role (str): The role of the new user (default is "user").
    """
    if username in db["users"]:
        raise HTTPException(status_code=400, detail="User already exists")
    db["users"][username] = {"username": username, "role": role}
    logger.info(f"New user created: {username} with role {role}")
    return {"message": f"User '{username}' created successfully", "role": role}

# Endpoint: List All Users
@app.get("/users/")
async def list_users(db: dict = Depends(get_database), logger: logging.Logger = Depends(get_logger)):
    """
    Lists all users in the database.
    """
    logger.info("Listing all users")
    return {"users": list(db["users"].keys())}
