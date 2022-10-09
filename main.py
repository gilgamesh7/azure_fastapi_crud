
from typing import Dict
from fastapi import FastAPI, status
import uvicorn

from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import urllib

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def create_database_connection()-> None:
    # Get database password from key vault
    key_vault_name = "kv-fastapi-crud-exercise"
    vault_uri = "https://kv-fastapi-crud-exercise.vault.azure.net/"
    secret_name = "fast-api-crud-db-password"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_uri, credential=credential)

    db_password = client.get_secret(secret_name).value

    # Create a Azure SQL(ODBC) engine instance
    connection_string = (
        'DRIVER=ODBC Driver 17 for SQL Server;'
        'SERVER=tcp:sql-fastapi-crud-exercise.database.windows.net;'
        'PORT=1433;'
        'DATABASE=sqldb-fastapi-crud-exercise;'
        'UID=fastapicrudadmin;'
        f'PWD={db_password};'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )   
    params = urllib.parse.quote_plus(connection_string)
    connection_uri = "mysql+pyodbc:///?odbc_connect=%s" % params
    azure_db_engine=  create_engine(connection_uri,echo=True)

    # Create a DeclarativeMeta instance
    Base = declarative_base()

    # Define To Do class inheriting from Base
    class ToDo(Base):
        __tablename__ = 'todolist'
        ToDoId = Column(Integer, primary_key=True)
        Task =  Column(String(50))

    # create a new database session
    session = Session(bind=azure_db_engine, expire_on_commit=False)

    # get the todo item with the given id
    todo = session.query(ToDo).get(1)

    print(f"todo item with id: {todo.id} and task: {todo.task}")

    # close the session
    session.close()

    # # Create the database
    # Base.metadata.create_all(azure_db_engine)
    # print("Created engine")

create_database_connection()



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




if __name__ == "__main__":
    uvicorn.run("main:app")