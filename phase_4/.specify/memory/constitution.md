<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles: All principles replaced with project-specific ones
- Added sections: Architecture Rules, Agent Rules, State Management, Delivery Rules
- Removed sections: Previous general principles
- Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
- Follow-up TODOs: None
-->
# Phase III AI-Powered Todo Chatbot Constitution

## Core Principles

### Spec-driven development only
All development must follow the spec-driven development methodology. No implementation before specification. All features MUST trace back to a spec.

### Stateless backend architecture
The backend API MUST be stateless. Server restarts MUST NOT break conversations. All state is persisted in the database, not in memory or session state.

### All AI actions must go through MCP tools
AI agents MUST interact with the system ONLY through MCP tools. The agent NEVER directly accesses database and can ONLY interact via MCP tools.

### No business logic inside the agent
Business logic lives inside MCP tools. Decision-making lives inside the AI agent, but business logic is externalized to maintain separation of concerns.

### Database is the single source of truth
Conversation state MUST be persisted in the database. Database access is via SQLModel only. The database is the authoritative source for all data.

### Production-ready code quality
All code must meet production-ready quality standards. This includes proper error handling, testing, security considerations, and performance optimization.

### Authentication-driven messaging
System must never send a chat message without a verified authenticated userId. Frontend MUST derive userId ONLY from auth session, never from assumptions. Backend MUST reject chat requests without JWT user context. Auth state MUST be resolved before ChatKit initialization.

### Cross-Origin Resource Sharing (CORS) requirements
Backend MUST allow cross-origin requests from the deployed frontend. All auth endpoints MUST support OPTIONS preflight requests. CORS configuration MUST be environment-aware and adapt to deployment scenarios. No auth request should fail due to missing Access-Control-Allow-Origin headers. Authentication flows MUST work seamlessly across different deployment domains.

## Architecture Rules
- Frontend MUST use OpenAI ChatKit only
- Backend MUST use FastAPI (Python)
- AI logic MUST use OpenAI Agents SDK
- MCP server MUST use Official MCP SDK
- ORM MUST be SQLModel only
- Database MUST be Neon Serverless PostgreSQL
- Authentication MUST use Better Auth
- Chat endpoint MUST be stateless
- Backend MUST support CORS for frontend deployment scenarios
- All auth endpoints MUST support OPTIONS preflight requests
- CORS configuration MUST be environment-aware and dynamic

## Agent Rules
- Agent NEVER directly accesses database
- Agent can ONLY interact via MCP tools
- Agent MUST confirm every successful action to the user
- Agent MUST gracefully handle errors
- Agent MUST infer intent from natural language

## State Management
- Conversation state MUST be persisted in database
- MCP tools MUST be stateless and store state only in the database
- Chat endpoint MUST hold no memory between requests
- Server restarts MUST NOT break conversations

## Delivery Rules
- Must produce working chatbot
- Must support resume after server restart
- Must include specs folder with complete specifications
- Must include database migrations
- Must include comprehensive README

## Governance
All development follows the spec-driven development process with clear separation of concerns. FastAPI routes handle HTTP only, business logic lives inside MCP tools, decision-making lives inside the AI agent, and database access is via SQLModel only. All write actions MUST be confirmed to the user, and errors MUST be handled gracefully. Authentication via Better Auth is mandatory, and user data MUST be scoped by user_id. Chat messaging MUST require verified authentication, with userId derived ONLY from auth session. Backend MUST validate JWT user context before processing chat requests. Auth state MUST be resolved before ChatKit initialization. Backend MUST support CORS for cross-origin requests from frontend deployments, and all auth endpoints MUST support OPTIONS preflight requests to ensure seamless authentication across different deployment domains.

**Version**: 2.1.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-30