from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import urllib

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Create a DeclarativeMeta instance
Base = declarative_base()

# Define To Do class inheriting from Base
class ToDo(Base):
    __tablename__ = 'todolist'
    ToDoId = Column(Integer, primary_key=True)
    Task =  Column(String(50))

def create_database_connection()-> Session:
    # Get database password from key vault
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
    connection_uri = f"mssql+pyodbc:///?odbc_connect={params}"
    azure_db_engine = create_engine(connection_uri,echo=False)

    return Session(azure_db_engine)

def get_todo_item_by_id(session: Session, id: int)-> str:
    with session:
        # get the todo item with the given id
        todo = session.query(ToDo).get(id)

    return f"todo item with id: {todo.ToDoId} and task: {todo.Task}"


session = create_database_connection()
print(get_todo_item_by_id(session, 1))