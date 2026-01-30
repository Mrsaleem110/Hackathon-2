# Implementation Plan: Authentication Fixes for Chat Messaging

**Branch**: `003-auth-fixes` | **Date**: 2026-01-30 | **Spec**: [pending]

**Input**: Feature specification from `/specs/003-auth-fixes/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of authentication verification and enforcement for chat messaging system. This includes verifying Better Auth session contains user.id on frontend, enforcing auth guards before ChatKit mounts, normalizing JWT payload on backend, implementing fail-fast mechanisms, and redeploying with corrected environment and auth flow.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/ES6+
**Primary Dependencies**: FastAPI, React 18, Better Auth, SQLModel, OpenAI ChatKit
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest, Jest
**Target Platform**: Web application (frontend + backend)
**Project Type**: Web
**Performance Goals**: <200ms p95 auth verification, secure JWT validation
**Constraints**: JWT user context required for all chat requests, frontend userId derived from auth session only
**Scale/Scope**: Individual user sessions, authenticated chat messaging

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-driven development compliance
- [ ] Specification exists in `/specs/[feature-name]/spec.md` before any implementation
- [ ] All features trace back to a spec requirement
- [ ] User stories and acceptance criteria clearly defined

### Architecture compliance
- [ ] Backend is stateless (no session state, no in-memory persistence)
- [ ] Database is single source of truth (SQLModel ORM only)
- [ ] MCP tools handle all business logic (not in agent)
- [ ] Frontend uses OpenAI ChatKit only
- [ ] Backend uses FastAPI (Python)
- [ ] AI logic uses OpenAI Agents SDK
- [ ] MCP server uses Official MCP SDK
- [ ] Database is Neon Serverless PostgreSQL
- [ ] Authentication uses Better Auth
- [ ] Chat endpoint is stateless
- [X] System must never send a chat message without a verified authenticated userId
- [X] Frontend MUST derive userId ONLY from auth session, never from assumptions
- [X] Backend MUST reject chat requests without JWT user context
- [X] Auth state MUST be resolved before ChatKit initialization

### Agent compliance
- [ ] Agent NEVER directly accesses database
- [ ] Agent ONLY interacts via MCP tools
- [ ] Agent confirms successful actions to user
- [ ] Agent gracefully handles errors
- [ ] Agent infers intent from natural language

### State management compliance
- [X] Conversation state persisted in database
- [X] MCP tools are stateless
- [X] Chat endpoint holds no memory between requests
- [X] Server restarts do not break conversations

### Delivery compliance
- [ ] Working chatbot produced
- [ ] Resume after server restart supported
- [ ] Specs folder with complete specifications included
- [ ] Database migrations included
- [ ] Comprehensive README included

## Project Structure

### Documentation (this feature)

```text
specs/003-auth-fixes/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── auth/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── contexts/
│   ├── hooks/
│   └── config/
└── tests/
```

**Structure Decision**: Web application with separate backend and frontend directories to maintain clear separation of concerns between API server and client application.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |

## Implementation Phases

### Phase 0: Research & Analysis
1. Verify current Better Auth session structure contains user.id
2. Analyze ChatKit mounting process and authentication timing
3. Examine JWT payload normalization requirements
4. Document current error handling for missing userId

### Phase 1: Design & Implementation
1. Implement frontend auth guard to verify user.id exists in session
2. Add auth state resolution before ChatKit component mounts
3. Normalize JWT payload to ensure consistent user_id/sub mapping
4. Implement fail-fast mechanism with clear error messages for missing userId
5. Update deployment configuration with corrected environment variables

### Phase 2: Testing & Validation
1. Unit tests for authentication verification functions
2. Integration tests for protected chat endpoints
3. End-to-end tests for auth flow before ChatKit initialization
4. Deployment validation on Vercel with corrected auth flow