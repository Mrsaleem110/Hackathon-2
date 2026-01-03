from sqlmodel import SQLModel
from app.models.user import User
from app.models.item import Item
from app.models.session import Session
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from sqlalchemy import create_engine

# This approach manually gets the table definitions
def generate_postgres_schema():
    print("-- PostgreSQL Schema for Todo App --")

    # Create a PostgreSQL dialect instance
    dialect = postgresql.dialect()

    # Print CREATE TABLE statements for each table
    for table in SQLModel.metadata.sorted_tables:
        print(f"-- Table: {table.name}")
        create_stmt = CreateTable(table)
        compiled_sql = create_stmt.compile(dialect=dialect)
        print(str(compiled_sql) + ";\n")

if __name__ == "__main__":
    generate_postgres_schema()