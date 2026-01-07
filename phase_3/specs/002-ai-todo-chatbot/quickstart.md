# Quickstart Guide: AI-Powered Todo Chatbot (Phase III)

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL (or Neon Serverless PostgreSQL account)
- Better Auth account (or setup for local development)
- OpenAI API key
- MCP SDK setup

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env):**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
OPENAI_API_KEY=your_openai_api_key
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_auth_secret
BETTER_AUTH_URL=http://localhost:3000
```

**Frontend (.env):**
```env
VITE_CHATKIT_DOMAIN_KEY=your_chatkit_domain_key
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Database Setup

```bash
# Run database migrations
cd backend
alembic upgrade head
```

### 4. MCP Server Setup

```bash
# Start MCP server
cd mcp
python -m src.server.main
```

### 5. Backend Server Setup

```bash
# Start backend server
cd backend
uvicorn src.api.main:app --reload --port 8000
```

### 6. Frontend Setup

```bash
# Start frontend
cd frontend
npm run dev
```

## Running the Application

1. Start the MCP server: `cd mcp && python -m src.server.main`
2. Start the backend: `cd backend && uvicorn src.api.main:app --reload --port 8000`
3. Start the frontend: `cd frontend && npm run dev`
4. Access the application at `http://localhost:5173`

## Testing the Application

### Unit Tests

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

### Integration Tests

```bash
# Run integration tests
cd backend
pytest tests/integration/
```

## Key Endpoints

- `POST /api/{user_id}/chat` - Main chat endpoint for natural language task management
- `GET /api/health` - Health check endpoint

## MCP Tools Available

- `add_task` - Add a new task
- `list_tasks` - List all tasks for a user
- `complete_task` - Mark a task as complete
- `delete_task` - Delete a task
- `update_task` - Update an existing task

## Troubleshooting

### Common Issues

1. **Database Connection Issues**: Ensure your PostgreSQL server is running and credentials are correct
2. **MCP Server Not Responding**: Check that the MCP server is running and properly configured
3. **Frontend Cannot Connect**: Verify that backend is running on the correct port and CORS is configured

### Development Mode

For development, use the `--reload` flag with uvicorn to automatically restart the server when code changes.