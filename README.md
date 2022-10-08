# azure_fastapi_crud

## Links
- [Building A Simple CRUD Application With FastAPI](https://www.gormanalysis.com/blog/building-a-simple-crud-application-with-fastapi/)
- [VDI - Swagger Documentation](http://127.0.0.1:8000/docs)
- [Create ODBC engine fot Azure SQL in SQLAlchemy](https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pyodbc)

## Installation
### Initial
- python3 -m venv venv --upgrade-deps
- pip install pipenv
- pipenv install fastapi
- pipenv install "uvicorn[standard]"
- pipenv install pyodbc
- pipenv install sqlalchemy
- pipenv install azure-identity
- pipenv install azure-keyvault-secrets
- 

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
# Get access for app to Azure Keyvault
1. Register your app with Azure Active Directory 
    1. Azure Active Directory
    1. App Registrations
    1. New Registration
    1. Name the app (fastapi-crud-exercise)
    1. Note down for running from laptop
        1. AZURE_CLIENT_ID
        1. AZURE_TENANT_ID
    1. Certificates and Secrets
    1. New Client Secret
    1. Give it a name (fastapi-crud-exercise)
    1. Note down "Value" for running from laptop : AZURE_CLIENT_SECRET