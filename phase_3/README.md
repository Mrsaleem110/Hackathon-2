# Phase 3: Todo AI Chat

This project implements an AI-powered chat interface for managing todos using natural language commands.

## Features

- Natural language processing for todo management
- AI-powered chat interface using OpenAI
- MCP tools for task operations (add, list, complete, delete, update)
- Conversation history persistence
- Session resumption after restart

## Architecture

### Backend Structure
```
backend/
├── app/
│   ├── chat/
│   │   └── routes.py        # /api/{user_id}/chat
│   ├── agents/
│   │   └── todo_agent.py
│   ├── mcp/
│   │   ├── server.py
│   │   └── tools.py
│   ├── models/
│   │   ├── task.py          # Phase 2 reuse
│   │   ├── conversation.py
│   │   └── message.py
│   └── db/
│       └── database.py
```

### Frontend Structure
```
frontend/
├── chatkit/
│   └── ChatUI.tsx
```

## Setup Instructions

### Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

3. Run the backend server:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Set up Stream Chat environment variables:
```bash
# Copy the example environment file
cp .env.local.example .env.local

# Add your Stream Chat API credentials
NEXT_PUBLIC_STREAM_API_KEY=your_stream_api_key_here
NEXT_PUBLIC_STREAM_USER_TOKEN=your_stream_user_token_here
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000/chat`

## API Endpoints

- `POST /api/{user_id}/chat` - Send a message to the AI chatbot
- `GET /api/{user_id}/chat/history` - Get conversation history

## MCP Tools

The system implements the following MCP tools:
- `add_task` - Add a new task
- `list_tasks` - List existing tasks
- `complete_task` - Mark a task as completed
- `delete_task` - Delete a task
- `update_task` - Update an existing task