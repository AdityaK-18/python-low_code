from fastapi import FastAPI
import asyncio  # For simulating time-consuming tasks

app = FastAPI()

# Root route
@app.get("/")
async def read_root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Asynchronous FastAPI Application!"}

# Simulate a time-consuming task
@app.get("/simulate-task/")
async def simulate_task(duration: int = 2):
    """
    Simulates a time-consuming task like a database query or API call.

    Args:
        duration (int): The duration (in seconds) for the task simulation. Default is 2 seconds.

    Returns:
        dict: A message confirming task completion with the duration.
    """
    await asyncio.sleep(duration)  # Simulate a time delay
    return {"message": f"Task completed in {duration} seconds"}

# Handle multiple asynchronous requests efficiently
@app.get("/multiple-tasks/")
async def handle_multiple_tasks():
    """
    Simulates handling multiple tasks concurrently using asyncio.gather().

    Returns:
        dict: A message confirming the completion of all tasks.
    """
    async def task_1():
        await asyncio.sleep(2)
        return "Task 1 completed"

    async def task_2():
        await asyncio.sleep(3)
        return "Task 2 completed"

    async def task_3():
        await asyncio.sleep(1)
        return "Task 3 completed"

    # Run tasks concurrently
    results = await asyncio.gather(task_1(), task_2(), task_3())
    return {"results": results}
