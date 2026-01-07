# AI-Powered Todo Chatbot (Phase III)

An AI-powered todo chatbot that enables users to manage tasks using natural language through an intelligent chat interface.

## Overview

This project implements a conversational todo management system where users can interact with an AI assistant using natural language to:
- Add new tasks
- List existing tasks
- Mark tasks as complete
- Update task details
- Delete tasks

The system follows a clean architecture with:
- Frontend: OpenAI ChatKit UI
- Backend: FastAPI server with stateless architecture
- MCP Server: Official MCP SDK handling business logic
- Database: Neon PostgreSQL with SQLModel ORM

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │    MCP Server   │
│  (ChatKit UI)   │───▶│   (FastAPI)      │───▶│  (MCP Tools)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                            │
                            ▼
                      ┌─────────────────┐
                      │   Database      │
                      │ (Neon PostgreSQL)│
                      └─────────────────┘
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- OpenAI API key
- OpenAI ChatKit domain key (for production deployment)

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Linux/Mac: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your environment variables
6. Run database migrations: `alembic upgrade head`
7. Start the server: `uvicorn src.api.main:app --reload --port 8000`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Create a `.env` file with your environment variables
4. Start the development server: `npm run dev`

### MCP Server Setup
1. Navigate to the mcp directory: `cd mcp`
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Start the MCP server: `python -m src.server.main`

### OpenAI ChatKit Domain Allowlist Configuration (Required for Production)

Before deploying your chatbot frontend to production, you must configure OpenAI's domain allowlist for security:

1. Deploy your frontend first to get a production URL:
   - Vercel: `https://your-app.vercel.app`
   - GitHub Pages: `https://username.github.io/repo-name`
   - Custom domain: `https://yourdomain.com`

2. Add your domain to OpenAI's allowlist:
   - Navigate to: https://platform.openai.com/settings/organization/security/domain-allowlist
   - Click "Add domain"
   - Enter your frontend URL (without trailing slash)
   - Save changes

3. Get your ChatKit domain key:
   - After adding the domain, OpenAI will provide a domain key
   - Add this key to your frontend environment variables

### Frontend Environment Variables
Create a `.env` file in the frontend directory:

```
VITE_CHATKIT_DOMAIN_KEY=your-chatkit-domain-key-here
VITE_API_BASE_URL=http://localhost:8000  # For local development
# For production, update to your backend URL
```

### Backend Environment Variables
Create a `.env` file in the backend directory:

```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
OPENAI_API_KEY=your_openai_api_key
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_auth_secret
BETTER_AUTH_URL=http://localhost:3000
```

Note: The hosted ChatKit option only works after adding the correct domains under Security → Domain Allowlist. Local development (`localhost`) typically works without this configuration.

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
OPENAI_API_KEY=your_openai_api_key
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_auth_secret
BETTER_AUTH_URL=http://localhost:3000
```

### Frontend (.env)
```
VITE_CHATKIT_DOMAIN_KEY=your_chatkit_domain_key
VITE_API_BASE_URL=http://localhost:8000
```

## API Endpoints

- `POST /api/{user_id}/chat` - Process natural language chat messages

## Development

### Running Tests
- Backend: `cd backend && pytest tests/`
- Frontend: `cd frontend && npm test`

### Database Migrations
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`

## Deployment

The application is designed to be deployed with:
- Frontend: Static hosting (Vercel, Netlify, etc.)
- Backend: Containerized with Docker (see Dockerfile)
- MCP Server: Containerized with Docker
- Database: Neon Serverless PostgreSQL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Specify your license here]