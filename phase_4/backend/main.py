from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Todo Chatbot Backend")

class HealthResponse(SQLModel):
    status: str
    version: str = "1.0.0"

@app.get("/")
def read_root():
    return {"message": "AI Todo Chatbot Backend is running!"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint to verify the backend is running properly
    """
    return HealthResponse(status="healthy", version="1.0.0")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todo_db")
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

def get_session():
    with Session(engine) as session:
        yield session

# Example model for Todo items
class TodoItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False

# Include other routes here as needed
@app.get("/todos")
def get_todos(session: Session = Depends(get_session)):
    todos = session.query(TodoItem).all()
    return todos

@app.post("/todos")
def create_todo(todo: TodoItem, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)