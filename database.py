from sqlalchemy import inspect, create_engine,Column, Integer, String, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import urllib

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from logging import Logger

# Create a DeclarativeMeta instance
Base = declarative_base()

# Define To Do class inheriting from Base
class ToDo(Base):
    __tablename__ = 'todolist'
    ToDoId = Column(Integer, primary_key=True)
    Task =  Column(String(50))


def create_database_engine()-> engine:
    try:
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

        # Create the database
        if not inspect(azure_db_engine).has_table('todolist'):
            print("Creating table")
            Base.metadata.create_all(azure_db_engine)
        else:
            print("Table already exists")

        return azure_db_engine
    except Exception as err:
        print(f"{err}")


def create_todo_record(task: str, logger: Logger)-> int:
    try:
        engine = create_database_engine()

        with Session(bind=engine, expire_on_commit=False) as session:
            tododb = ToDo(Task=task)

            session.add(tododb)
            session.commit()

            id = tododb.ToDoId

        engine.dispose()

        return id
    except Exception as error:
        logger.exception(f"{error}")
        raise error

def get_todo_record(id: int, logger:Logger)-> str:
    try:
        engine = create_database_engine()

        with Session(bind=engine, expire_on_commit=False) as session:
            todo = session.query(ToDo).get(id)

        engine.dispose()

        if todo is None:
            raise Exception(f"No data found for ID {id}")

        return todo
    except Exception as error:
        logger.exception(f"{error}")
        raise error