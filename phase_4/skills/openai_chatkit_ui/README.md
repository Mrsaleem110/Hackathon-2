# OpenAI ChatKit UI Skill

This skill provides an embeddable OpenAI ChatKit UI that connects to OpenAI-hosted Agent workflows.

## Features

- Embeddable React chat widget
- Secure session management via backend API
- Connection to OpenAI Agent workflows
- Automatic response streaming
- File attachment support
- Tool invocation and widgets

## Setup

### Frontend Dependencies

```bash
npm install @openai/chatkit-react
```

### Backend Dependencies

All required dependencies are already included in the project.

## Usage

### Frontend Component

```jsx
import ChatKitWidget from './components/ChatKitWidget';

function App() {
  return (
    <div className="App">
      <h1>My App with ChatKit</h1>
      <ChatKitWidget
        workflowId="your-openai-workflow-id"
        userId="current-user-id"
      />
    </div>
  );
}
```

### Custom Hook Usage

```jsx
import useChatSession from './hooks/useChatSession';

function MyComponent() {
  const {
    sessionData,
    isLoading,
    error,
    createSession
  } = useChatSession();

  const handleStartChat = async () => {
    try {
      await createSession('user-123', 'workflow-456');
    } catch (err) {
      console.error('Failed to create session:', err);
    }
  };

  if (isLoading) return <div>Loading chat...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>Chat ready!</div>
  );
}
```

## API Endpoints

### POST /api/chatkit/session
Create a new ChatKit session
```json
{
  "userId": "user-identifier",
  "workflowId": "workflow-identifier",
  "metadata": {}
}
```

### POST /api/chatkit/session/{session_id}/refresh
Refresh an existing session token

### GET /api/chatkit/session/{session_id}/validate
Validate if a session is still active

### GET /api/chatkit/workflows/{workflow_id}
Get workflow configuration

## Configuration

Set environment variables:
```bash
CHATKIT_SECRET=your-secret-key-here
```

The frontend configuration is in `public/chatkit-config.json`.

## Running the Application

1. Start the backend:
```bash
cd backend
uvicorn src.api.main:app --reload
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

## Security

- Sessions are secured with JWT tokens
- Tokens expire after 1 hour (configurable)
- All API calls require authentication
- Server generates tokens, client never handles secrets