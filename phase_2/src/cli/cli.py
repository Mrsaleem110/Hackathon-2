'''
CLI module for the todo console application.

This module handles all user input and output, renders menus and task listings,
and performs input validation as specified in the plan.
'''

import sys
from typing import Optional
from ..services.task_service import TaskService


class TodoCLI:
    '''
    Command-line interface for the todo application.
    Handles user input/output and delegates to the task service.
    '''

    def __init__(self, task_service: TaskService):
        '''Initialize the CLI with a task service.'''
        self.task_service = task_service

    def display_menu(self):
        '''Display the main menu options to the user.'''
        print("\n" + "="*50)
        print("TODO CONSOLE APPLICATION")
        print("="*50)
        print("Available commands:")
        print("  create    - Create a new task")
        print("  list      - View all tasks")
        print("  update    - Update an existing task")
        print("  delete    - Delete a task")
        print("  toggle    - Toggle task completion status")
        print("  exit      - Quit the application")
        print("="*50)

    def get_user_input(self, prompt: str) -> str:
        '''Get input from the user with a prompt.'''
        return input(prompt).strip()

    def create_task(self):
        '''Handle task creation command.'''
        print("\n--- Create New Task ---")
        title = self.get_user_input("Enter task title: ")

        if not title:
            print("Error: Title cannot be empty.")
            return

        description = self.get_user_input("Enter task description (optional, press Enter to skip): ")
        if not description:  # If user pressed Enter without typing
            description = None

        try:
            task = self.task_service.create_task(title, description)
            print(f"Task created successfully with ID: {task.id}")
        except ValueError as e:
            print(f"Error creating task: {e}")

    def list_tasks(self):
        '''Handle task listing command.'''
        print("\n--- All Tasks ---")
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        # Print header
        print(f"{'ID':<4} | {'Title':<20} | {'Description':<30} | {'Status':<12}")
        print("-" * 70)

        # Print each task
        for task in tasks:
            status = "Complete" if task.is_completed else "Incomplete"
            description = task.description if task.description else ""
            # Truncate long titles/descriptions for display
            title_display = (task.title[:17] + "...") if len(task.title) > 20 else task.title
            desc_display = (description[:27] + "...") if len(description) > 30 else description
            print(f"{task.id:<4} | {title_display:<20} | {desc_display:<30} | {status:<12}")

    def update_task(self):
        '''Handle task update command.'''
        print("\n--- Update Task ---")
        try:
            task_id_input = self.get_user_input("Enter task ID to update: ")
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        # Check if task exists
        existing_task = self.task_service.get_task(task_id)
        if not existing_task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        print(f"Current task: {existing_task.title}")
        if existing_task.description:
            print(f"Current description: {existing_task.description}")

        # Get new title (or keep current if empty input)
        new_title_input = self.get_user_input(f"Enter new title (current: '{existing_task.title}', press Enter to keep current): ")
        new_title = new_title_input if new_title_input else existing_task.title

        # Get new description (or keep current if empty input)
        current_desc = existing_task.description if existing_task.description else ""
        new_desc_input = self.get_user_input(f"Enter new description (current: '{current_desc}', press Enter to keep current): ")
        new_description = new_desc_input if new_desc_input else existing_task.description
        if not new_desc_input and existing_task.description is None:
            new_description = None

        updated_task = self.task_service.update_task(task_id, new_title, new_description)
        if updated_task:
            print(f"Task {task_id} updated successfully.")
        else:
            print(f"Error: Failed to update task {task_id}.")

    def delete_task(self):
        '''Handle task deletion command.'''
        print("\n--- Delete Task ---")
        try:
            task_id_input = self.get_user_input("Enter task ID to delete: ")
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        success = self.task_service.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} does not exist.")

    def toggle_task(self):
        '''Handle task completion toggle command.'''
        print("\n--- Toggle Task Completion ---")
        try:
            task_id_input = self.get_user_input("Enter task ID to toggle: ")
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        task = self.task_service.toggle_task_completion(task_id)
        if task:
            status = "Complete" if task.is_completed else "Incomplete"
            print(f"Task {task_id} marked as {status}.")
        else:
            print(f"Error: Task with ID {task_id} does not exist.")

    def run(self):
        '''Run the main CLI loop.'''
        print("Welcome to the Todo Console Application!")
        while True:
            self.display_menu()
            command = self.get_user_input("\nEnter command: ").lower()

            if command == "create":
                self.create_task()
            elif command == "list":
                self.list_tasks()
            elif command == "update":
                self.update_task()
            elif command == "delete":
                self.delete_task()
            elif command == "toggle":
                self.toggle_task()
            elif command == "exit":
                print("Thank you for using the Todo Console Application. Goodbye!")
                sys.exit(0)
            else:
                print(f"Error: Unknown command '{command}'. Please try again.")