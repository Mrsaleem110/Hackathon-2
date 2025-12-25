'''
Task model for the todo console application.

This module defines the Task domain entity with all required attributes
and ensures ID immutability and state integrity as specified in the plan.
'''

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)  # Using frozen=True to ensure immutability
class Task:
    '''
    Represents a single todo task with immutable ID and modifiable state.

    Attributes:
        id: Integer, unique and immutable sequential identifier
        title: String, mandatory task title
        description: String, optional task description
        is_completed: Boolean, completion status (default: False)
    '''

    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool = False

    def __post_init__(self):
        '''Validate task attributes after initialization.'''
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        if self.description and len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

    def with_updated_title(self, new_title: str) -> 'Task':
        '''Create a new task with updated title.'''
        return Task(
            id=self.id,
            title=new_title,
            description=self.description,
            is_completed=self.is_completed
        )

    def with_updated_description(self, new_description: Optional[str]) -> 'Task':
        '''Create a new task with updated description.'''
        return Task(
            id=self.id,
            title=self.title,
            description=new_description,
            is_completed=self.is_completed
        )

    def with_toggled_completion(self) -> 'Task':
        '''Create a new task with toggled completion status.'''
        return Task(
            id=self.id,
            title=self.title,
            description=self.description,
            is_completed=not self.is_completed
        )