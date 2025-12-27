'''
Main entry point for the todo console application.

This module controls application lifecycle and implements the main execution loop
as specified in the architectural plan.
'''

from .services.task_service import TaskService
from .cli.cli import TodoCLI


def main():
    '''
    Application entry point.
    Initializes services and starts the main application loop.
    '''
    print("Initializing Todo Console Application...")

    # Initialize the task service (in-memory storage)
    task_service = TaskService()

    # Initialize the CLI interface
    cli = TodoCLI(task_service)

    print("Application initialized successfully!")

    # Start the main application loop
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
        exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Terminating application.")
        exit(1)


if __name__ == "__main__":
    main()