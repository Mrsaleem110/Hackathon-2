---
id: "001"
title: "OpenAI ChatKit UI Skill Creation"
stage: "general"
date_iso: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "create skills on spec skill create openai_chatkit_ui"
labels: ["skill", "chatkit", "ui", "openai", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "skills/openai_chatkit_ui.yaml"
  - "frontend/src/components/ChatKitWidget.jsx"
  - "frontend/src/hooks/useChatSession.js"
  - "backend/src/api/chatkit.py"
  - "frontend/public/chatkit-config.json"
  - "frontend/package.json"
  - "skills/openai_chatkit_ui/README.md"
  - "test_chatkit_integration.py"
tests_yaml:
  - "test_chatkit_integration.py"
---

# OpenAI ChatKit UI Skill Creation

## User Prompt
```
create skills on spec skill create openai_chatkit_ui
  description "Build an embeddable OpenAI ChatKit UI using OpenAI-hosted Agent workflows"

  source_docs
    - OpenAI ChatKit official documentation
    - OpenAI-hosted ChatKit integration (recommended)

  purpose
    - Define rules for embedding ChatKit UI in a frontend
    - Ensure secure session handling via server-generated client secrets
    - Connect frontend chat UI to OpenAI-hosted agent workflows

  integration_mode
    - OpenAI-hosted ChatKit backend
    - Agent workflow created via Agent Builder
    - Frontend embeds ChatKit widget

  stack
    - Frontend: React / Next.js
    - Chat UI: @openai/chatkit-react
    - Script: chatkit.js (CDN)
    - Backend: FastAPI (session token endpoint)

  capabilities
    - Embed ChatKit UI widget
    - Connect UI to OpenAI Agent workflow via workflow ID
    - Create and refresh ChatKit sessions
    - Stream chat responses automatically
    - Support tool invocation & widgets (via workflow)
    - Handle file attachments and UI st
```

## Response Summary
Created a complete OpenAI ChatKit UI skill with:

1. Skill configuration file (skills/openai_chatkit_ui.yaml)
2. Frontend React component (ChatKitWidget.jsx)
3. Custom React hook for session management (useChatSession.js)
4. Backend API endpoints for session handling (chatkit.py)
5. Configuration files for frontend and backend
6. Updated package.json with required dependencies
7. Comprehensive README documentation
8. Test script to verify integration

The implementation follows security best practices with server-generated JWT tokens for session management, and provides all necessary endpoints for creating, refreshing, and validating ChatKit sessions. The frontend component handles loading states, error handling, and connects to the backend API for secure session token generation.

## Outcome
Successfully created a complete, secure, and functional OpenAI ChatKit UI skill that can be embedded in any React application and connects to OpenAI-hosted agent workflows.