# Data Model: Todo Console Application

## Task Entity

### Attributes
- `id`: Integer (unique, immutable sequential identifier)
- `title`: String (mandatory, non-empty)
- `description`: String (optional, nullable)
- `is_completed`: Boolean (default: False)

### Invariants
- ID must be unique within the application
- ID must be assigned sequentially starting from 1
- Title must not be empty or None
- Title length must be between 1-255 characters
- Description length must not exceed 1000 characters if provided

### State Transitions
- Initial state: `is_completed = False`
- Toggle operation: `is_completed = not is_completed`

## Task Collection

### In-Memory Storage
- Python list for ordered storage of Task objects
- Python dictionary for O(1) lookup by ID
- Synchronized access to maintain consistency

### Operations
- Create: Add new Task to both list and dictionary
- Read: Retrieve Task by ID from dictionary
- Update: Modify existing Task attributes
- Delete: Remove Task from both list and dictionary
- List: Return all Tasks from the list