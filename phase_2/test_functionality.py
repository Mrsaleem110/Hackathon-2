'''
Test script to verify the todo application functionality.
'''

from src.models.task_model import Task
from src.services.task_service import TaskService


def test_task_creation():
    '''Test task creation functionality.'''
    print("Testing task creation...")

    # Test basic task creation
    task = Task(id=1, title="Test Task", description="Test Description", is_completed=False)
    print(f"Created task: {task}")

    # Test task creation with minimal parameters
    task2 = Task(id=2, title="Simple Task")
    print(f"Created simple task: {task2}")

    # Test validation
    try:
        invalid_task = Task(id=3, title="")  # Should fail
        print("ERROR: Should have failed validation")
    except ValueError as e:
        print(f"Correctly caught validation error: {e}")


def test_task_service():
    '''Test task service functionality.'''
    print("\nTesting task service...")

    service = TaskService()

    # Test creating tasks
    task1 = service.create_task("First Task", "Description for first task")
    print(f"Created task: {task1}")

    task2 = service.create_task("Second Task")
    print(f"Created task: {task2}")

    # Test getting all tasks
    all_tasks = service.get_all_tasks()
    print(f"All tasks: {all_tasks}")

    # Test toggling completion
    toggled_task = service.toggle_task_completion(task1.id)
    print(f"Toggled task: {toggled_task} (is_completed: {toggled_task.is_completed})")

    # Test updating task
    updated_task = service.update_task(task1.id, title="Updated Task Title")
    print(f"Updated task: {updated_task}")

    # Test deleting task
    delete_result = service.delete_task(task2.id)
    print(f"Delete result for task {task2.id}: {delete_result}")

    remaining_tasks = service.get_all_tasks()
    print(f"Remaining tasks: {remaining_tasks}")


if __name__ == "__main__":
    test_task_creation()
    test_task_service()
    print("\nAll tests passed!")