# Implementation Plan: Authentication Fixes for Chat Messaging

**Branch**: `003-auth-fixes` | **Date**: 2026-01-31 | **Spec**: [pending]

**Input**: Feature specification from `/specs/003-auth-fixes/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of authentication verification and enforcement for chat messaging system. This includes verifying Better Auth session contains user.id on frontend, enforcing auth guards before ChatKit mounts, normalizing JWT payload on backend, implementing fail-fast mechanisms, and redeploying with corrected environment and auth flow. Additionally, comprehensive CORS configuration is implemented to ensure authentication works properly between frontend and backend deployed on different Vercel domains.

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
- [X] Specification exists in `/specs/[feature-name]/spec.md` before any implementation
- [X] All features trace back to a spec requirement
- [X] User stories and acceptance criteria clearly defined

### Architecture compliance
- [X] Backend is stateless (no session state, no in-memory persistence)
- [X] Database is single source of truth (SQLModel ORM only)
- [X] MCP tools handle all business logic (not in agent)
- [X] Frontend uses OpenAI ChatKit only
- [X] Backend uses FastAPI (Python)
- [X] AI logic uses OpenAI Agents SDK
- [X] MCP server uses Official MCP SDK
- [X] Database is Neon Serverless PostgreSQL
- [X] Authentication uses Better Auth
- [X] Chat endpoint is stateless
- [X] System must never send a chat message without a verified authenticated userId
- [X] Frontend MUST derive userId ONLY from auth session, never from assumptions
- [X] Backend MUST reject chat requests without JWT user context
- [X] Auth state MUST be resolved before ChatKit initialization
- [X] Backend MUST support CORS for frontend deployment scenarios
- [X] All auth endpoints MUST support OPTIONS preflight requests
- [X] CORS configuration MUST be environment-aware and dynamic

### Agent compliance
- [X] Agent NEVER directly accesses database
- [X] Agent ONLY interacts via MCP tools
- [X] Agent confirms successful actions to user
- [X] Agent gracefully handles errors
- [X] Agent infers intent from natural language

### State management compliance
- [X] Conversation state persisted in database
- [X] MCP tools are stateless
- [X] Chat endpoint holds no memory between requests
- [X] Server restarts do not break conversations

### Delivery compliance
- [X] Working chatbot produced
- [X] Resume after server restart supported
- [X] Specs folder with complete specifications included
- [X] Database migrations included
- [X] Comprehensive README included

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
│   │   └── main.py      # FastAPI app with CORS configuration
│   └── auth/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── contexts/
│   ├── hooks/
│   ├── utils/
│   │   └── envValidator.js  # Environment validation
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
5. Analyze current CORS configuration and cross-origin request handling

### Phase 1: Design & Implementation
1. Implement frontend auth guard to verify user.id exists in session
2. Add auth state resolution before ChatKit component mounts
3. Normalize JWT payload to ensure consistent user_id/sub mapping
4. Implement fail-fast mechanism with clear error messages for missing userId
5. Configure comprehensive CORS settings to allow frontend Vercel domain
6. Ensure all auth endpoints support OPTIONS preflight requests
7. Update deployment configuration with corrected environment variables

### Phase 2: Testing & Validation
1. Unit tests for authentication verification functions
2. Integration tests for protected chat endpoints
3. End-to-end tests for auth flow before ChatKit initialization
4. CORS preflight request tests
5. Cross-origin authentication flow tests
6. Deployment validation on Vercel with corrected auth flow

## CORS Configuration Details

### FastAPI CORSMiddleware Settings
- **allow_origins**: Comprehensive list including localhost and Vercel domains
- **allow_credentials**: True (to support authentication cookies/tokens)
- **allow_methods**: ["*"] (to support GET, POST, PUT, DELETE, OPTIONS, etc.)
- **allow_headers**: ["*"] (to support Authorization, Content-Type, etc.)

### Special Handling
- Dynamic Vercel domain matching for preview deployments
- OPTIONS preflight request support for all routes
- Exception handler CORS headers to ensure all error responses include proper CORS headers
- Environment-aware configuration supporting both development and production

## Authentication Flow Verification

### Frontend Requirements
- Verify user.id exists in auth session before enabling chat functionality
- Wait for complete auth state resolution before mounting ChatInterface
- Include userId in all chat API requests
- Proper error handling when auth fails

### Backend Requirements
- Validate JWT and extract user ID for all chat operations
- Reject requests without valid JWT token
- Normalize JWT payload to handle different field names (sub vs user_id)
- Ensure CORS headers are present for all responses including errors