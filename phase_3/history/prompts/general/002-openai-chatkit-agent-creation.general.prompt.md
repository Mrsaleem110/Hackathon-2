---
id: "002"
title: "OpenAI ChatKit UI Agent Creation"
stage: "general"
date_iso: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "create openai chatkit subagent spec agent create openai_chatkit_ui_agent"
labels: ["agent", "chatkit", "openai", "ui", "session-management"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "agents/openai_chatkit_ui_agent.yaml"
  - "backend/src/api/chatkit_agent.py"
  - "frontend/src/components/ChatKitProvider.jsx"
  - "frontend/src/hooks/useChatKit.js"
  - "frontend/src/components/ChatKitUI.jsx"
  - "test_chatkit_agent_integration.py"
  - "backend/src/api/main.py"
tests_yaml:
  - "test_chatkit_agent_integration.py"
---

# OpenAI ChatKit UI Agent Creation

## User Prompt
```
create openai chatkit subagent spec agent create openai_chatkit_ui_agent
  role "OpenAI ChatKit UI Implementer"

  uses skill openai_chatkit_ui

  responsibilities
    - Implement FastAPI endpoint to create ChatKit sessions
    - Use OpenAI SDK to generate ChatKit client_secret
    - Embed ChatKit UI in React / Next.js frontend
    - Load ChatKit JS script correctly
    - Initialize useChatKit hook
    - Render ChatKit component
    - Implement session refresh logic

  implementation_steps
    - Create /api/chatkit/session backend endpoint
    - Pass workflow ID to OpenAI ChatKit sessions API
    - Return client_secret securely
    - Install @openai/chatkit-react
    - Mount ChatKit UI in frontend component

  output
    - Working backend ChatKit session endpoint
    - Frontend ChatKit UI connected to OpenAI workflow
    - Code follows official ChatKit documentation exactly

end
```

## Response Summary
Created a complete OpenAI ChatKit UI agent with:

1. Agent configuration file (agents/openai_chatkit_ui_agent.yaml)
2. Backend API endpoints for ChatKit sessions with OpenAI SDK integration (chatkit_agent.py)
3. Frontend components:
   - ChatKitProvider.jsx: Context provider for ChatKit functionality
   - useChatKit.js: Custom hook for session management with auto-refresh
   - ChatKitUI.jsx: Main UI component that embeds the ChatKit interface
4. Updated main API router to include the new agent endpoints
5. Comprehensive test script to verify integration

The implementation includes secure session management with JWT tokens, automatic session refresh 5 minutes before expiry, proper error handling, and follows security best practices by generating client secrets server-side.

## Outcome
Successfully created a complete OpenAI ChatKit UI agent that can create and manage ChatKit sessions using the OpenAI SDK, with frontend components that properly embed the ChatKit UI and handle session lifecycle management.