# Data Model: Advanced Cloud Deployment

## Task Entity

**Fields:**
- `id`: UUID (primary key)
- `title`: String (required, max 200 characters)
- `description`: Text (optional)
- `status`: Enum (active, completed, archived)
- `priority`: Enum (low, medium, high)
- `due_date`: DateTime (optional)
- `reminder_time`: DateTime (optional)
- `recurrence_pattern`: JSON (optional, structure: {type: daily/weekly/monthly, interval: int, end_date: DateTime})
- `tags`: Array of strings (max 10 tags)
- `created_at`: DateTime
- `updated_at`: DateTime
- `completed_at`: DateTime (optional)
- `parent_task_id`: UUID (optional, for subtasks)

**Validation Rules:**
- Title must be 1-200 characters
- Priority must be one of: low, medium, high
- Due date must be in the future if set
- Reminder time must be before due date if both are set
- Tags must be 1-50 characters each, max 10 tags

**State Transitions:**
- active → completed (when marked complete)
- completed → active (when unmarked)
- any → archived (when deleted)

## User Entity

**Fields:**
- `id`: UUID (primary key)
- `email`: String (unique, required)
- `name`: String (required)
- `preferences`: JSON (optional, structure: {default_reminder_time: int, default_priority: string, theme: string})
- `created_at`: DateTime
- `updated_at`: DateTime

**Validation Rules:**
- Email must be valid email format and unique
- Name must be 1-100 characters

## TaskSeries Entity (for recurring tasks)

**Fields:**
- `id`: UUID (primary key)
- `title`: String (required)
- `description`: Text (optional)
- `recurrence_pattern`: JSON (required, structure: {type: daily/weekly/monthly, interval: int, end_date: DateTime, days_of_week: array, day_of_month: int})
- `created_at`: DateTime
- `updated_at`: DateTime

## Notification Entity

**Fields:**
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to User)
- `task_id`: UUID (foreign key to Task)
- `notification_type`: Enum (reminder, due_soon, overdue, recurring)
- `scheduled_time`: DateTime
- `sent_time`: DateTime (optional)
- `status`: Enum (scheduled, sent, failed)
- `channel`: Enum (in_app, email, push)
- `created_at`: DateTime

## Tag Entity

**Fields:**
- `id`: UUID (primary key)
- `name`: String (unique, required, max 50 characters)
- `color`: String (optional, hex color code)
- `user_id`: UUID (foreign key to User, for user-specific tags)
- `created_at`: DateTime

**Validation Rules:**
- Name must be 1-50 characters
- Color must be valid hex format if provided
- Tag names must be unique per user

## Conversation History Entity

**Fields:**
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to User)
- `session_id`: String (required)
- `message`: Text (required)
- `role`: Enum (user, assistant)
- `timestamp`: DateTime
- `metadata`: JSON (optional, for additional context)

**Relationships:**
- Task ↔ User (many-to-one)
- Task ↔ TaskSeries (many-to-one, optional)
- Task ↔ Tags (many-to-many through task_tags junction table)
- Notification ↔ User (many-to-one)
- Notification ↔ Task (many-to-one)
- Tag ↔ User (many-to-one)