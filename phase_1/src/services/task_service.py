'''
Task service for the todo console application.

This module implements the business logic for task management,
including in-memory storage and all CRUD operations as specified.
'''

from typing import Dict, List, Optional
from ..models.task_model import Task


class TaskService:
    '''
    Service class that manages all business logic for task operations.
    Implements in-memory task registry with sequential ID assignment.
    '''

    def __init__(self):
        '''Initialize the in-memory task storage.'''
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        '''
        Create a new task with the given title and optional description.

        Args:
            title: The task title (mandatory)
            description: The task description (optional)

        Returns:
            The created Task object with assigned ID and initial "Incomplete" status

        Raises:
            ValueError: If title is invalid
        '''
        # Create a new task with the next available ID
        new_task = Task(
            id=self._next_id,
            title=title,
            description=description,
            is_completed=False
        )

        # Add to storage
        self._tasks[self._next_id] = new_task

        # Increment the next ID for the following task
        self._next_id += 1

        return new_task

    def get_task(self, task_id: int) -> Optional[Task]:
        '''
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        '''
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        '''
        Retrieve all tasks in the system.

        Returns:
            A list of all Task objects, sorted by ID
        '''
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        '''
        Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task object if successful, None if task doesn't exist
        '''
        if task_id not in self._tasks:
            return None

        current_task = self._tasks[task_id]

        # Use provided values or keep existing ones
        new_title = title if title is not None else current_task.title
        new_description = description if description is not None else current_task.description

        # Create updated task
        updated_task = Task(
            id=current_task.id,
            title=new_title,
            description=new_description,
            is_completed=current_task.is_completed
        )

        # Update storage
        self._tasks[task_id] = updated_task

        return updated_task

    def delete_task(self, task_id: int) -> bool:
        '''
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was successfully deleted, False if it didn't exist
        '''
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        '''
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object if successful, None if task doesn't exist
        '''
        if task_id not in self._tasks:
            return None

        current_task = self._tasks[task_id]

        # Create task with toggled completion status
        updated_task = Task(
            id=current_task.id,
            title=current_task.title,
            description=current_task.description,
            is_completed=not current_task.is_completed
        )

        # Update storage
        self._tasks[task_id] = updated_task

        return updated_task