# Data Model: AI-Powered Todo Chatbot (Phase III)

## Entity Definitions

### Task Entity
**Description**: Represents a user's todo item with all necessary attributes for task management.

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the task
- `user_id` (String/UUID): Foreign key linking to the user who owns this task
- `title` (String): Title or brief description of the task
- `description` (Text, optional): Detailed description of the task
- `completed` (Boolean): Status indicating if the task is completed (default: false)
- `created_at` (DateTime): Timestamp when the task was created
- `updated_at` (DateTime): Timestamp when the task was last updated

**Validation Rules**:
- `title` is required and must be between 1-255 characters
- `user_id` must reference an existing user
- `completed` defaults to false when creating a new task

**State Transitions**:
- New task: `completed = false`
- Task completed: `completed = true`
- Task uncompleted: `completed = false`

### Conversation Entity
**Description**: Represents a chat session between a user and the AI, maintaining conversation context.

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the conversation
- `user_id` (String/UUID): Foreign key linking to the user who owns this conversation
- `created_at` (DateTime): Timestamp when the conversation was started
- `updated_at` (DateTime): Timestamp when the conversation was last active

**Validation Rules**:
- `user_id` must reference an existing user
- `created_at` is set automatically on creation

### Message Entity
**Description**: Represents an individual message in a conversation, storing both user and AI messages.

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the message
- `conversation_id` (Integer/UUID): Foreign key linking to the conversation
- `user_id` (String/UUID): Foreign key linking to the user who sent the message
- `role` (String): Role of the message sender ('user' or 'assistant')
- `content` (Text): The actual content of the message
- `created_at` (DateTime): Timestamp when the message was created

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `user_id` must reference an existing user
- `role` must be either 'user' or 'assistant'
- `content` is required and must not be empty

## Entity Relationships

### Task Relationships
- Task belongs to one User (via `user_id`)
- One User has many Tasks

### Conversation Relationships
- Conversation belongs to one User (via `user_id`)
- One User has many Conversations
- One Conversation has many Messages

### Message Relationships
- Message belongs to one Conversation (via `conversation_id`)
- Message belongs to one User (via `user_id`)
- One Conversation has many Messages
- One User has many Messages (across all conversations)

## Database Schema

```sql
-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Indexes for Performance

```sql
-- Indexes for efficient querying
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## SQLModel Implementation

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationBase(SQLModel):
    pass

class Conversation(ConversationBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MessageBase(SQLModel):
    conversation_id: uuid.UUID
    user_id: str
    role: str  # 'user' or 'assistant'
    content: str

class Message(MessageBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```