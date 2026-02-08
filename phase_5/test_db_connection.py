#!/usr/bin/env python3
"""
Test script to diagnose the database connection and task retrieval issue
"""

import os
from dotenv import load_dotenv
load_dotenv()

from backend.src.database.connection import get_session
from backend.src.services.task_service import TaskService
from backend.src.models.task import Task
from sqlmodel import select
import traceback

def test_database_connection():
    print("Testing database connection and task retrieval...")

    try:
        # Get a session
        session_gen = get_session()
        session = next(session_gen)

        print("Connected to database successfully!")

        # Try to execute a simple query
        statement = select(Task).where(Task.user_id == "test-user")
        result = session.exec(statement)
        tasks = result.all()

        print(f"Query executed successfully. Found {len(tasks)} tasks.")

        # Try to call the service method
        user_tasks = TaskService.get_tasks_by_user(session, "6b99c796-a485-433c-a0da-d497d5a57b9c")
        print(f"Service method executed successfully. Found {len(user_tasks)} tasks for test user.")

        session.close()
        print("Test completed successfully!")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    test_database_connection()