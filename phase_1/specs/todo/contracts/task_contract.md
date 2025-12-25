# Task Contract: Todo Console Application

## Task Creation Contract

### Request
- **Method**: create_task(title: str, description: str = None)
- **Parameters**:
  - `title`: String, mandatory, 1-255 characters
  - `description`: String, optional, max 1000 characters
- **Preconditions**:
  - Title must not be empty
  - Title must not exceed 255 characters
  - If provided, description must not exceed 1000 characters

### Response
- **Success**: Task object with assigned unique ID and initial "Incomplete" status
- **Error**: ValidationError with descriptive message
- **Postconditions**:
  - New task added to collection
  - Task ID is next sequential number
  - Task status is "Incomplete"

## Task Retrieval Contract

### Request
- **Method**: get_task(task_id: int)
- **Parameters**:
  - `task_id`: Integer, unique identifier
- **Preconditions**:
  - Task with given ID must exist

### Response
- **Success**: Task object with all attributes
- **Error**: TaskNotFoundError with descriptive message

## Task Update Contract

### Request
- **Method**: update_task(task_id: int, title: str = None, description: str = None)
- **Parameters**:
  - `task_id`: Integer, unique identifier
  - `title`: String, optional, 1-255 characters if provided
  - `description`: String, optional, max 1000 characters if provided
- **Preconditions**:
  - Task with given ID must exist
  - If title provided, it must not exceed 255 characters
  - If description provided, it must not exceed 1000 characters

### Response
- **Success**: Updated Task object
- **Error**: TaskNotFoundError or ValidationError with descriptive message

## Task Deletion Contract

### Request
- **Method**: delete_task(task_id: int)
- **Parameters**:
  - `task_id`: Integer, unique identifier
- **Preconditions**:
  - Task with given ID must exist

### Response
- **Success**: Boolean True indicating successful deletion
- **Error**: TaskNotFoundError with descriptive message
- **Postconditions**:
  - Task removed from collection
  - Task ID remains reserved (not reused)

## Task Toggle Contract

### Request
- **Method**: toggle_task_completion(task_id: int)
- **Parameters**:
  - `task_id`: Integer, unique identifier
- **Preconditions**:
  - Task with given ID must exist

### Response
- **Success**: Updated Task object with toggled completion status
- **Error**: TaskNotFoundError with descriptive message