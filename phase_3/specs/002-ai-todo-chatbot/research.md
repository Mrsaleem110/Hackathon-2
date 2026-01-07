# Research: AI-Powered Todo Chatbot (Phase III)

## Research Summary

This document captures the research and decisions made for implementing the AI-Powered Todo Chatbot (Phase III) feature.

## Decision: Technology Stack Selection
**Rationale**: Based on the project constitution and requirements, we've selected the following technology stack:
- Frontend: OpenAI ChatKit (as required by constitution)
- Backend: FastAPI with Python (as required by constitution)
- Database: Neon Serverless PostgreSQL with SQLModel ORM (as required by constitution)
- AI Logic: OpenAI Agents SDK (as required by constitution)
- MCP Server: Official MCP SDK (as required by constitution)
- Authentication: Better Auth (as required by constitution)

**Alternatives considered**:
- Alternative frameworks like Django, Flask were considered but FastAPI was chosen as it's constitutionally required
- Alternative databases like MongoDB, MySQL were considered but PostgreSQL was chosen as constitutionally required
- Alternative AI frameworks were considered but OpenAI Agents SDK was chosen as constitutionally required

## Decision: Architecture Pattern
**Rationale**: We're implementing a clean architecture pattern with:
- Frontend (ChatKit) handles UI and user interactions
- Backend (FastAPI) handles API requests and coordinates between frontend and MCP
- MCP Server handles all business logic through tools
- Database (PostgreSQL) stores all persistent data

This ensures clear separation of concerns and compliance with the constitution that requires all business logic to be in MCP tools, not in the AI agent.

**Alternatives considered**:
- Monolithic architecture was considered but rejected to maintain separation of concerns
- Direct database access from agent was considered but rejected as it violates constitution

## Decision: State Management Strategy
**Rationale**: Following the constitution's requirement for stateless architecture:
- All conversation state is persisted in the database
- The chat endpoint is stateless and holds no memory between requests
- MCP tools are stateless and store state only in the database
- Server restarts will not break conversations as all state is in the database

**Alternatives considered**:
- In-memory session storage was considered but rejected due to stateless architecture requirement
- Client-side storage was considered but rejected for security and consistency reasons

## Decision: MCP Tool Design
**Rationale**: The MCP server will expose the following tools as required by the specification:
- add_task: Creates new tasks in the database
- list_tasks: Retrieves tasks for a user
- complete_task: Updates task completion status
- delete_task: Removes tasks from the database
- update_task: Modifies existing task properties

Each tool follows the stateless pattern and only interacts with the database.

**Alternatives considered**:
- Combined tools were considered but individual tools provide better modularity
- Direct database access from agent was considered but rejected as it violates constitution

## Decision: Authentication and Authorization
**Rationale**: Using Better Auth as required by constitution to handle user authentication and ensure proper user_id scoping for all data access. This ensures users can only access their own tasks and conversations.

**Alternatives considered**:
- Custom authentication was considered but Better Auth is constitutionally required
- JWT-only approach was considered but Better Auth provides better security practices

## Decision: Error Handling Strategy
**Rationale**: Implementing comprehensive error handling at multiple levels:
- MCP tools return structured error responses
- AI agent handles errors gracefully and provides user-friendly messages
- Database operations include proper validation and error reporting
- Frontend displays appropriate error states

**Alternatives considered**:
- Simple error messages were considered but comprehensive error handling is needed for good UX
- Silent error handling was considered but rejected for transparency

## Decision: Conversation Management
**Rationale**: Using conversation_id to maintain conversation context across requests while keeping the endpoint stateless. The conversation_id is stored in the database and referenced in each request to maintain continuity.

**Alternatives considered**:
- Session-based approach was considered but rejected due to stateless requirement
- Client-only tracking was considered but rejected for server-side consistency