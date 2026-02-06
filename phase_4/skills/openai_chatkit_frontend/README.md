# OpenAI ChatKit Frontend Skills

This module provides skills for creating and managing OpenAI ChatKit frontend components.

## Overview

The OpenAI ChatKit Frontend skills provide a comprehensive set of tools for:
- Creating React components for ChatKit UI
- Creating React hooks for managing ChatKit connections
- Creating ChatKit sessions via backend API
- Generating integration code for frontend applications

## Skills

### `create_chatkit_ui_component`
Create a React component for the ChatKit UI.

**Parameters:**
- `component_name`: Name of the component to create (e.g., "ChatKitUI", "ChatKitProvider")
- `props`: Properties to configure the component (optional)

### `create_chatkit_hook`
Create a React hook for managing ChatKit connections.

**Parameters:**
- `hook_name`: Name of the hook to create (e.g., "useChatKit")
- `config`: Configuration for the hook (optional)

### `create_chatkit_session`
Create a ChatKit session using the backend API.

**Parameters:**
- `workflow_id`: ID of the workflow
- `user_id`: ID of the user
- `metadata`: Additional metadata for the session (optional)

### `generate_chatkit_integration_code`
Generate code for integrating ChatKit into the frontend.

**Parameters:**
- `integration_type`: Type of integration ('component', 'hook', 'provider', etc.)
- `config`: Configuration for the integration (optional)

### `write_chatkit_component_to_file`
Write a ChatKit component to a file.

**Parameters:**
- `component_name`: Name of the component to create
- `file_path`: Path where the component should be saved
- `props`: Properties to configure the component (optional)

## Examples

### Creating a ChatKit UI Component
```python
from skills.openai_chatkit_frontend.openai_chatkit_frontend_skills import create_chatkit_ui_component

component_result = await create_chatkit_ui_component(
    component_name="ChatKitUI",
    props={
        "sessionId": null,
        "workflowId": null,
        "userId": null
    }
)
```

### Creating a useChatKit Hook
```python
from skills.openai_chatkit_frontend.openai_chatkit_frontend_skills import create_chatkit_hook

hook_result = await create_chatkit_hook(
    hook_name="useChatKit",
    config={
        "autoConnect": True,
        "reconnectAttempts": 3
    }
)
```

### Creating a ChatKit Session
```python
from skills.openai_chatkit_frontend.openai_chatkit_frontend_skills import create_chatkit_session

session_result = await create_chatkit_session(
    workflow_id="support-workflow",
    user_id="user-123",
    metadata={
        "department": "support",
        "priority": "high"
    }
)
```

### Generating Integration Code
```python
from skills.openai_chatkit_frontend.openai_chatkit_frontend_skills import generate_chatkit_integration_code

integration_result = await generate_chatkit_integration_code(
    integration_type="component",
    config={}
)
```

### Writing Component to File
```python
from skills.openai_chatkit_frontend.openai_chatkit_frontend_skills import write_chatkit_component_to_file

file_result = await write_chatkit_component_to_file(
    component_name="ChatKitUI",
    file_path="frontend/src/components/ChatKitUI.jsx",
    props={}
)
```

## Dependencies

- `react>=18.0.0`
- `@openai/chatkit-react`

## Installation

```bash
npm install react @openai/chatkit-react
```

## Testing

Run the example implementation:

```bash
python openai_chatkit_frontend_skills.py
```