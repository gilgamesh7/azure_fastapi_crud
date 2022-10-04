# azure_fastapi_crud

## Links
- [Building A Simple CRUD Application With FastAPI](https://www.gormanalysis.com/blog/building-a-simple-crud-application-with-fastapi/)
- [VDI - Swagger Documentation](http://127.0.0.1:8000/docs)

## Installation
### Initial
- python3 -m venv venv --upgrade-deps
- pip install pipenv
- pipenv install fastapi
- pipenv install "uvicorn[standard]"

### Packages to install
- See Pipfile

## Run the app
### VDI
- uvicorn main:app --reload

# Azure details
- Subscription : Mr.Spock
- Resource Group : rg-fastapi-crud
- SQL Server : sql-fastapi-crud-exercise
- SQL Database : sqldb-fastapi-crud-exercise

# Azure SQL DB Table
```
create table todolist
(
	ToDoId INT IDENTITY PRIMARY KEY,
	Task  NVARCHAR(128) NOT NULL
)
```