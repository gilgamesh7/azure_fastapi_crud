
from typing import Dict
from fastapi import FastAPI, status, HTTPException, Depends
import uvicorn

import logging

from pydantic import BaseModel, validator

from database import create_todo_record, get_todo_record, get_all_todo_records, update_todo_record


# Instantiate logging
logging.basicConfig(level=logging.INFO, format="[{asctime}] - {funcName} - {lineno} - {message}", style='{')
logger = logging.getLogger("fastapi_crud")

# Create ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str

    @validator('task')
    def must_contain_value(cls, task):
        if len(task) < 1 or task == "" or task is None :
            raise ValueError("Task must contain a value")
        
        return task

class ToDoIdRequest(BaseModel):
    id: int

    @validator('id')
    def id_has_to_be_over_zero(cls, id):
        if id <= 0 or not isinstance(id, int) :
            raise HTTPException(status_code=400, detail={"success":"n", "message":"ID has to be a positive integer"})

        return id

class ToDoUpdateRequest(BaseModel):
    id: int
    task: str

    @validator('id')
    def id_has_to_be_over_zero(cls, id):
        if id <= 0 or not isinstance(id, int) :
            raise HTTPException(status_code=400, detail={"success":"n", "message":"ID has to be a positive integer"})

        return id

    @validator('task')
    def must_contain_value(cls, task):
        if len(task) < 1 or task == "" or task is None :
            raise ValueError("Task must contain a value")
        
        return task


app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def root()-> Dict:
    return {"success":"y", "message":"In God We Trust!"}

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest)-> Dict:
    try:
        logger.info(f"Task : {todo.task}")

        id = create_todo_record(todo.task, logger)

        return {"success":"y", "message":f"Created ID {id}"}
    except Exception as error:
        logger.exception(f"Creation error {error}")
        raise HTTPException(status_code=400, detail={"success":"n", "message":f"Creation caused error : {error}"})

@app.get("/todo/{id}")
def read_todo(todo_id: ToDoIdRequest=Depends())-> Dict:
    try:
        logger.info(f"Getting record with Id {todo_id.id}")
        details = get_todo_record(todo_id.id, logger)

        return {"success":"y", "message":details}
    except Exception as error:
        logger.exception(f"Retrieval error {error}")
        raise HTTPException(status_code=400, detail={"success":"n", "message":f"Retrieval error : {error}"})

@app.put("/todo")
def update_todo(todo: ToDoUpdateRequest)-> str:
    try:
        logger.info(f"Updating record with Id {todo.id} and task {todo.task}")
        details = update_todo_record(todo.id, todo.task, logger)

        return {"success":"y", "message":details}
    except Exception as error:
        logger.exception(f"Retrieval error {error}")
        raise HTTPException(status_code=400, detail={"success":"n", "message":f"Retrieval error : {error}"})

@app.delete("/todo/{id}")
def delete_todo(id: int)-> str:
    return f"delete todo item {id}"

@app.get("/todo")
def read_todo_list()-> Dict:
    try:
        logger.info(f"Getting all To Do items")
        details = get_all_todo_records(logger)

        return {"success":"y", "message":details}
    except Exception as error:
        logger.exception(f"Retrieval error {error}")
        raise HTTPException(status_code=400, detail={"success":"n", "message":f"Retrieval error : {error}"})




if __name__ == "__main__":
    uvicorn.run("main:app")