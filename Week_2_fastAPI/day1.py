from fastapi import FastAPI

# Create an instance of the FastAPI application
app = FastAPI()

# Define a GET route
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Hello, World!"}

# Define a POST route
@app.post("/items/")
def create_item(name: str):
    """
    Endpoint to create an item. Accepts a query parameter 'name'.
    
    Args:
        name (str): The name of the item to create.
        
    Returns:
        dict: A message confirming the creation of the item.
    """
    return {"message": f"Item '{name}' has been created!"}
