---
id: 2
title: update-constitution-templates
stage: constitution
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Code
command: sp.constitution
labels: [constitution, governance, templates, compliance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---
## Prompt

```text
<<EOF
Project Name: Phase III AI-Powered Todo Chatbot

Core Principles:
- Spec-driven development only
- Stateless backend architecture
- All AI actions must go through MCP tools
- No business logic inside the agent
- Database is the single source of truth
- Production-ready code quality

Architecture Rules:
- Frontend uses OpenAI ChatKit only
- Backend uses FastAPI (Python)
- AI logic uses OpenAI Agents SDK
- MCP server uses Official MCP SDK
- ORM must be SQLModel
- Database must be Neon Serverless PostgreSQL
- Authentication via Better Auth
- Chat endpoint must be stateless

Agent Rules:
- Agent NEVER directly accesses database
- Agent can ONLY interact via MCP tools
- Agent must confirm every successful action
- Agent must gracefully handle errors
- Agent must infer intent from natural language

State Management:
- Conversation state persisted in database
- MCP tools are stateless
- Chat endpoint holds no memory between requests

Delivery Rules:
- Must produce working chatbot
- Must support resume after server restart
- Must include specs folder
- Must include database migrations
- Must include README

EOF
```

## Response snapshot

Updated the project constitution and aligned templates to ensure consistency with the new principles. The constitution at .specify/memory/constitution.md was already updated with the specific principles for the Phase III AI-Powered Todo Chatbot project. The following template files were updated to align with the constitution:

1. .specify/templates/plan-template.md: Added comprehensive constitution check section with specific compliance gates for spec-driven development, architecture compliance, agent compliance, state management compliance, and delivery compliance.

2. .specify/templates/spec-template.md: Updated functional requirements to include constitution compliance requirements (FR-001 through FR-012) and added a dedicated Constitution Compliance Requirements section (CC-001 through CC-005).

3. .specify/templates/tasks-template.md: Updated setup, foundational, and polish phases to include specific tasks that ensure constitution compliance, including database setup with SQLModel, authentication with Better Auth, MCP tools framework, and stateless architecture implementation.

All templates now reflect the project's core principles of spec-driven development, stateless architecture, MCP tool usage, and database as single source of truth.

## Outcome

- ✅ Impact: Aligned project templates with constitution to ensure consistent compliance
- 🧪 Tests: No tests required for this template update
- 📁 Files: Updated 4 files to ensure constitution consistency (.specify/memory/constitution.md, .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md)
- 🔁 Next prompts: Templates are now properly aligned with constitution for future feature development
- 🧠 Reflection: Template alignment ensures constitution principles are enforced throughout the development lifecycle

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A