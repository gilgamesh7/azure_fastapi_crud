
from typing import Dict
from fastapi import FastAPI, status

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def root()-> Dict:
    return {"message":"In God We Trust!"}

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo()-> str:
    return "created To Do Item"

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