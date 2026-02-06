# Implementation Plan: AI-Powered Todo Chatbot (Phase III)

**Branch**: `002-ai-todo-chatbot` | **Date**: 2026-01-06 | **Spec**: [specs/002-ai-todo-chatbot/spec.md](../specs/002-ai-todo-chatbot/spec.md)
**Input**: Feature specification from `/specs/002-ai-todo-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered todo chatbot that enables users to manage tasks using natural language. The system uses OpenAI Agents SDK to interpret natural language requests, routes all business logic through MCP tools, and maintains conversation state in a Neon PostgreSQL database. The frontend uses OpenAI ChatKit for the user interface.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript for frontend
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon PostgreSQL, Better Auth, OpenAI ChatKit
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (Linux server)
**Project Type**: Web (frontend + backend + MCP server)
**Performance Goals**: Handle 100 concurrent users, response time under 2 seconds
**Constraints**: <200ms p95 for database queries, <500MB memory, stateless backend
**Scale/Scope**: 10k users, 1M tasks, real-time conversation support

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-driven development compliance
- [x] Specification exists in `/specs/[feature-name]/spec.md` before any implementation
- [x] All features trace back to a spec requirement
- [x] User stories and acceptance criteria clearly defined

### Architecture compliance
- [x] Backend is stateless (no session state, no in-memory persistence)
- [x] Database is single source of truth (SQLModel ORM only)
- [x] MCP tools handle all business logic (not in agent)
- [x] Frontend uses OpenAI ChatKit only
- [x] Backend uses FastAPI (Python)
- [x] AI logic uses OpenAI Agents SDK
- [x] MCP server uses Official MCP SDK
- [x] Database is Neon Serverless PostgreSQL
- [x] Authentication uses Better Auth
- [x] Chat endpoint is stateless

### Agent compliance
- [x] Agent NEVER directly accesses database
- [x] Agent ONLY interacts via MCP tools
- [x] Agent confirms successful actions to user
- [x] Agent gracefully handles errors
- [x] Agent infers intent from natural language

### State management compliance
- [x] Conversation state persisted in database
- [x] MCP tools are stateless
- [x] Chat endpoint holds no memory between requests
- [x] Server restarts do not break conversations

### Delivery compliance
- [x] Working chatbot produced
- [x] Resume after server restart supported
- [x] Specs folder with complete specifications included
- [x] Database migrations included
- [x] Comprehensive README included

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-todo-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── types/
├── public/
├── package.json
└── README.md

backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   ├── database/
│   └── auth/
├── requirements.txt
├── alembic/
└── README.md

mcp/
├── src/
│   ├── tools/
│   ├── server/
│   └── config/
├── requirements.txt
└── README.md

specs/
├── 001-ai-todo-chatbot/
└── 002-ai-todo-chatbot/

migrations/
├── versions/
└── env.py

README.md
```

**Structure Decision**: Selected web application structure with separate frontend, backend, and MCP server components to maintain clear separation of concerns. The frontend uses OpenAI ChatKit, the backend uses FastAPI with stateless architecture, and the MCP server handles all business logic through Official MCP SDK.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |