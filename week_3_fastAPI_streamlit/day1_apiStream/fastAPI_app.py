from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    age: int
    grade: str

students = [
    {"id": 1, "name": "Alice", "age": 20, "grade": "A"},
    {"id": 2, "name": "Bob", "age": 22, "grade": "B"},
    {"id": 3, "name": "Charlie", "age": 21, "grade": "A"},
]

@app.get("/students")
def get_students():
    return students
