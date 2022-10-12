
from typing import Dict
from fastapi import FastAPI, status
import uvicorn

from pydantic import BaseModel

from database import create_todo_record

# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def root()-> Dict:
    return {"message":"In God We Trust!"}

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest)-> str:
    print(f"Task : {todo.task}")

    status = create_todo_record(todo.task)

    return status

@app.get("/todo/{id}")
def read_todo(id: int)-> str:
    return f"getting todo item with id : {id}"

@app.put("/todo/{id}")
def update_todo(id: int)-> str:
    return f"Updating todo item {id}"

@app.delete("/todo/{id}")
def delete_todo(id: int)-> str:
    return f"delete todo item {id}"

@app.get("/todo")
def read_todo_list()-> str:
    return "List of todo items"




if __name__ == "__main__":
    uvicorn.run("main:app")