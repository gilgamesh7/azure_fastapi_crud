from pydantic import BaseModel, validator
from fastapi import HTTPException

# Create ToDoRequest Base Model
class ToDo(BaseModel):
    ToDoId: int
    Task: str

    class Config:
        orm_mode = True

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

