#!/usr/bin/env python3
"""
Debug script to test the exact issue in the get_tasks endpoint
"""

import os
from dotenv import load_dotenv
load_dotenv()

from backend.src.database.connection import get_session
from backend.src.services.task_service import TaskService
from backend.src.auth import verify_custom_token
from sqlmodel import Session
import traceback

def debug_get_tasks():
    print("Debugging get_tasks functionality...")

    # Simulate the token verification
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2Yjk5Yzc5Ni1hNDg1LTQzM2MtYTBkYS1kNDk3ZDVhNTdiOWMiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJuYW1lIjoiVGVzdCBVc2VyIiwiZXhwIjoxNzY4NjU3Nzc2fQ.xlKlFvQbMWR4BAU2T4c62uMMR2UHi3Z7-PQUqldkxxs"

    try:
        print("1. Verifying token...")
        current_user = verify_custom_token(token)
        print(f"   Token verified successfully. User ID: {current_user.id}")

        print("2. Getting database session...")
        session_gen = get_session()
        session = next(session_gen)
        print("   Session obtained successfully")

        print("3. Calling TaskService.get_tasks_by_user...")
        tasks = TaskService.get_tasks_by_user(session, current_user.id)
        print(f"   Successfully retrieved {len(tasks)} tasks")

        # Convert tasks to dict for serialization (this is what FastAPI does)
        tasks_dict = [task.dict() for task in tasks]  # This might be the issue!
        print(f"   Successfully converted {len(tasks_dict)} tasks to dict")

        session.close()
        print("Test completed successfully!")
        return True

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_get_tasks()