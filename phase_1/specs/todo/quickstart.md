# Quickstart Guide: Todo Console Application

## Prerequisites
- Python 3.13 or newer
- Linux environment (WSL 2, Ubuntu 22.04 recommended)

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Ensure Python 3.13+ is available in your environment

## Running the Application
```bash
cd src
python main.py
```

## Available Commands
- `create` - Create a new task
- `list` - View all tasks
- `update` - Update an existing task
- `delete` - Delete a task
- `toggle` - Toggle task completion status
- `exit` - Quit the application

## Example Usage
```
> create
Title: Buy groceries
Description: Get milk, bread, and eggs
Task created with ID: 1

> list
ID | Title           | Description              | Status
1  | Buy groceries   | Get milk, bread, and eggs| Incomplete

> toggle 1
Task 1 marked as Complete

> list
ID | Title           | Description              | Status
1  | Buy groceries   | Get milk, bread, and eggs| Complete
```

## Development
To run tests:
```bash
python -m pytest tests/
```