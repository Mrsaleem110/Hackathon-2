# OpenAI ChatKit Frontend Subagent

This subagent specializes in creating and managing OpenAI ChatKit frontend components.

## Overview

The OpenAI ChatKit Frontend Subagent is a specialized agent that can:
- Create React components for ChatKit UI
- Create React hooks for managing ChatKit connections
- Create ChatKit sessions via backend API
- Generate integration code for frontend applications
- Write components directly to files
- Manage the lifecycle of frontend components

## Capabilities

- `create-chatkit-ui-component`: Create React components for ChatKit UI
- `create-chatkit-hook`: Create React hooks for managing connections
- `create-chatkit-session`: Create ChatKit sessions via backend API
- `generate-integration-code`: Generate integration code for frontend
- `write-component-to-file`: Write components directly to files
- `manage-frontend-components`: Track and manage component lifecycles

## Configuration

The subagent can be configured with:

- `default_frontend_framework`: Default frontend framework (default: "react")
- `default_chatkit_package`: Default ChatKit package (default: "@openai/chatkit-react")
- `enable_logging`: Enable detailed logging (default: true)

## Tasks

### `create_ui_component`
Create a ChatKit UI component.

**Parameters:**
- `component_name`: Name of the component to create (required)
- `props`: Properties to configure the component (optional)

### `create_hook`
Create a ChatKit hook.

**Parameters:**
- `hook_name`: Name of the hook to create (required)
- `config`: Configuration for the hook (optional)

### `create_session`
Create a ChatKit session.

**Parameters:**
- `workflow_id`: ID of the workflow (required)
- `user_id`: ID of the user (required)
- `metadata`: Additional metadata for the session (optional)

### `generate_integration`
Generate integration code.

**Parameters:**
- `integration_type`: Type of integration (required)
- `config`: Configuration for the integration (optional)

### `write_component_to_file`
Write a component to a file.

**Parameters:**
- `component_name`: Name of the component to create (required)
- `file_path`: Path where the component should be saved (required)
- `props`: Properties to configure the component (optional)

### `get_component_info`
Get information about a specific component.

**Parameters:**
- `component_id`: ID of the component to get information for (required)

### `list_components`
List all registered components (no parameters required).

### `get_session_info`
Get information about a specific session.

**Parameters:**
- `session_id`: ID of the session to get information for (required)

### `list_sessions`
List all registered sessions (no parameters required).

## Usage Examples

### Creating a UI Component
```
create_ui_component:
  component_name: "ChatKitUI"
  props:
    sessionId: null
    workflowId: null
    userId: null
```

### Creating a Hook
```
create_hook:
  hook_name: "useChatKit"
  config:
    autoConnect: true
    reconnectAttempts: 3
```

### Creating a Session
```
create_session:
  workflow_id: "support-workflow"
  user_id: "user-123"
  metadata:
    department: "support"
    priority: "high"
```

### Generating Integration Code
```
generate_integration:
  integration_type: "component"
  config: {}
```

### Writing Component to File
```
write_component_to_file:
  component_name: "ChatKitUI"
  file_path: "frontend/src/components/ChatKitUI.jsx"
  props: {}
```

## Dependencies

- `skills.openai_chatkit_frontend`

## Integration with Frontend

The subagent generates complete React components and hooks that can be directly integrated into your frontend application. The generated components include:

1. **ChatKitUI**: A complete UI component for the ChatKit interface
2. **useChatKit**: A custom hook for managing ChatKit connections
3. **ChatKitProvider**: A context provider for managing ChatKit state

These components are designed to work together and integrate with your existing React application architecture.