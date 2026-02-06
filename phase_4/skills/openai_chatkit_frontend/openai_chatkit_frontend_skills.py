"""
OpenAI ChatKit Frontend Skills
This module provides skills for creating and managing OpenAI ChatKit frontend components.
"""
import asyncio
import json
from typing import Dict, Any, Optional, List
import os
from pathlib import Path


class OpenAIChatKitFrontendSkills:
    """
    Skills for working with the OpenAI ChatKit frontend.
    These skills provide high-level operations for creating and managing ChatKit UI components.
    """

    def __init__(self):
        self.skill_name = "openai_chatkit_frontend_skills"
        self.description = "Skills for creating and managing OpenAI ChatKit frontend components"

    async def create_chatkit_ui_component(self, component_name: str, props: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a React component for the ChatKit UI.

        Args:
            component_name: Name of the component to create
            props: Properties to configure the component

        Returns:
            Dictionary containing component code or error information
        """
        try:
            if not component_name:
                return {
                    "error": "'component_name' is required"
                }

            # Normalize the component name for comparison
            normalized_name = component_name.lower().replace('_', '').replace('-', '')

            # Define the ChatKit UI component based on the name
            if normalized_name == "chatkitui":
                component_code = self._generate_chatkit_ui_component(props or {})
            elif normalized_name == "chatkitprovider":
                component_code = self._generate_chatkit_provider_component(props or {})
            else:
                component_code = self._generate_generic_component(component_name, props or {})

            return {
                "success": True,
                "component_name": component_name,
                "component_code": component_code,
                "message": f"ChatKit UI component '{component_name}' created successfully"
            }

        except Exception as e:
            return {"error": f"Failed to create ChatKit UI component: {str(e)}"}

    async def create_chatkit_hook(self, hook_name: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a React hook for managing ChatKit connections.

        Args:
            hook_name: Name of the hook to create
            config: Configuration for the hook

        Returns:
            Dictionary containing hook code or error information
        """
        try:
            if not hook_name:
                return {
                    "error": "'hook_name' is required"
                }

            # Normalize the hook name for comparison
            normalized_name = hook_name.lower().replace('_', '').replace('-', '')

            # Define the ChatKit hook based on the name
            if normalized_name == "usechatkit":
                hook_code = self._generate_use_chatkit_hook(config or {})
            else:
                hook_code = self._generate_generic_hook(hook_name, config or {})

            return {
                "success": True,
                "hook_name": hook_name,
                "hook_code": hook_code,
                "message": f"ChatKit hook '{hook_name}' created successfully"
            }

        except Exception as e:
            return {"error": f"Failed to create ChatKit hook: {str(e)}"}

    async def create_chatkit_session(self, workflow_id: str, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a ChatKit session using the backend API.

        Args:
            workflow_id: ID of the workflow
            user_id: ID of the user
            metadata: Additional metadata for the session

        Returns:
            Dictionary containing session data or error information
        """
        try:
            # This would typically call the backend API
            # For this implementation, we'll simulate the session creation
            import uuid
            from datetime import datetime

            session_id = str(uuid.uuid4())

            # Simulate creating a client secret (in real implementation, this would be from backend)
            client_secret = f"sk-chatkit-test-{uuid.uuid4()}-secret"

            session_data = {
                "session_id": session_id,
                "client_secret": client_secret,
                "workflow_id": workflow_id,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow().timestamp() + 3600),
                "metadata": metadata or {}
            }

            return {
                "success": True,
                "session_data": session_data,
                "message": f"ChatKit session created successfully with ID: {session_id}"
            }

        except Exception as e:
            return {"error": f"Failed to create ChatKit session: {str(e)}"}

    async def generate_chatkit_integration_code(self, integration_type: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate code for integrating ChatKit into the frontend.

        Args:
            integration_type: Type of integration ('component', 'hook', 'provider', etc.)
            config: Configuration for the integration

        Returns:
            Dictionary containing integration code or error information
        """
        try:
            if not integration_type:
                return {
                    "error": "'integration_type' is required"
                }

            if integration_type.lower() == "component":
                code = self._generate_chatkit_component_integration(config or {})
            elif integration_type.lower() == "hook":
                code = self._generate_chatkit_hook_integration(config or {})
            elif integration_type.lower() == "provider":
                code = self._generate_chatkit_provider_integration(config or {})
            else:
                code = self._generate_generic_integration(integration_type, config or {})

            return {
                "success": True,
                "integration_type": integration_type,
                "integration_code": code,
                "message": f"ChatKit {integration_type} integration code generated successfully"
            }

        except Exception as e:
            return {"error": f"Failed to generate ChatKit integration code: {str(e)}"}

    async def write_chatkit_component_to_file(self, component_name: str, file_path: str, props: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Write a ChatKit component to a file.

        Args:
            component_name: Name of the component to create
            file_path: Path where the component should be saved
            props: Properties to configure the component

        Returns:
            Dictionary containing success/error information
        """
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Generate the component code
            component_result = await self.create_chatkit_ui_component(component_name, props)

            if not component_result.get("success"):
                return component_result

            # Write the component to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(component_result["component_code"])

            return {
                "success": True,
                "file_path": file_path,
                "message": f"ChatKit component '{component_name}' written to {file_path}"
            }

        except Exception as e:
            return {"error": f"Failed to write ChatKit component to file: {str(e)}"}

    def _generate_chatkit_ui_component(self, props: Dict[str, Any]) -> str:
        """Generate the ChatKit UI React component."""
        return '''import React, { useState, useEffect } from 'react';
import { useChatKit } from \'../hooks/useChatKit\';

const ChatKitUI = ({
  sessionId = null,
  workflowId = null,
  userId = null,
  onMessage = () => {},
  onError = () => {},
  className = ""
}) => {
  const {
    connect,
    disconnect,
    sendMessage,
    messages,
    isConnected,
    isLoading
  } = useChatKit();

  const [inputValue, setInputValue] = useState('');
  const [sessionData, setSessionData] = useState(null);

  useEffect(() => {
    if (sessionId || (workflowId && userId)) {
      initializeSession();
    }
  }, [sessionId, workflowId, userId]);

  const initializeSession = async () => {
    try {
      // Connect to ChatKit using session data
      const sessionInfo = await getSessionData();
      setSessionData(sessionInfo);

      await connect({
        sessionId: sessionInfo.session_id,
        clientSecret: sessionInfo.client_secret,
        ...props
      });
    } catch (error) {
      onError(error);
    }
  };

  const getSessionData = async () => {
    // In a real implementation, this would call the backend API
    // to get session information
    if (sessionId) {
      // Retrieve existing session
      return await fetch(`/api/chatkit/session/${sessionId}`).then(r => r.json());
    } else {
      // Create new session
      return await fetch('/api/chatkit/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workflowId, userId })
      }).then(r => r.json());
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || !isConnected) return;

    try {
      await sendMessage(inputValue);
      setInputValue('');
      onMessage(inputValue);
    } catch (error) {
      onError(error);
    }
  };

  return (
    <div className={`chatkit-ui ${className}`}>
      <div className="chatkit-header">
        <h3>ChatKit UI</h3>
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </div>
      </div>

      <div className="chatkit-messages">
        {isLoading ? (
          <div className="loading">Connecting...</div>
        ) : messages.length === 0 ? (
          <div className="empty-state">No messages yet. Start a conversation!</div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`message ${msg.senderId === userId ? 'sent' : 'received'}`}>
              <div className="message-content">{msg.text}</div>
              <div className="message-time">{msg.timestamp}</div>
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleSubmit} className="chatkit-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={!isConnected}
        />
        <button type="submit" disabled={!isConnected || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatKitUI;
'''

    def _generate_chatkit_provider_component(self, props: Dict[str, Any]) -> str:
        """Generate the ChatKit Provider React component."""
        return '''import React, { createContext, useContext, useReducer } from 'react';

const ChatKitContext = createContext();

const chatKitReducer = (state, action) => {
  switch (action.type) {
    case 'SET_CONNECTION_STATUS':
      return { ...state, isConnected: action.payload };
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] };
    case 'SET_MESSAGES':
      return { ...state, messages: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

export const ChatKitProvider = ({ children, config = {} }) => {
  const [state, dispatch] = useReducer(chatKitReducer, {
    isConnected: false,
    messages: [],
    isLoading: false,
    error: null
  });

  const value = {
    state,
    dispatch,
    connect: async (connectionParams) => {
      dispatch({ type: 'SET_LOADING', payload: true });
      try {
        // Implementation would connect to ChatKit service
        // This is a simplified version
        console.log('Connecting to ChatKit with params:', connectionParams);

        // Simulate connection
        setTimeout(() => {
          dispatch({ type: 'SET_CONNECTION_STATUS', payload: true });
          dispatch({ type: 'SET_LOADING', payload: false });
        }, 500);
      } catch (error) {
        dispatch({ type: 'SET_ERROR', payload: error.message });
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    },
    disconnect: () => {
      dispatch({ type: 'SET_CONNECTION_STATUS', payload: false });
    },
    sendMessage: async (text) => {
      if (!state.isConnected) throw new Error('Not connected to ChatKit');

      const message = {
        id: Date.now().toString(),
        text,
        senderId: config.userId || 'current-user',
        timestamp: new Date().toISOString()
      };

      dispatch({ type: 'ADD_MESSAGE', payload: message });
      // In real implementation, send to ChatKit service
    }
  };

  return (
    <ChatKitContext.Provider value={value}>
      {children}
    </ChatKitContext.Provider>
  );
};

export const useChatKitContext = () => {
  const context = useContext(ChatKitContext);
  if (!context) {
    throw new Error('useChatKitContext must be used within a ChatKitProvider');
  }
  return context;
};
'''

    def _generate_use_chatkit_hook(self, config: Dict[str, Any]) -> str:
        """Generate the useChatKit React hook."""
        return '''import { useState, useCallback, useEffect } from 'react';
import { useChatKitContext } from './ChatKitProvider';

export const useChatKit = () => {
  const { state, dispatch, connect, disconnect, sendMessage } = useChatKitContext();
  const [wsConnection, setWsConnection] = useState(null);

  // Expose the state and functions
  const { isConnected, messages, isLoading, error } = state;

  const connectToChatKit = useCallback(async (connectionParams) => {
    await connect(connectionParams);
  }, [connect]);

  const disconnectFromChatKit = useCallback(() => {
    if (wsConnection) {
      wsConnection.close();
      setWsConnection(null);
    }
    disconnect();
  }, [wsConnection, disconnect]);

  const sendMessageToChatKit = useCallback(async (text) => {
    if (!isConnected) {
      throw new Error('Cannot send message: not connected to ChatKit');
    }

    // Send via WebSocket if available, otherwise use REST API
    if (wsConnection && wsConnection.readyState === WebSocket.OPEN) {
      wsConnection.send(JSON.stringify({ type: 'MESSAGE', text }));
    } else {
      // Fallback to REST API
      return await sendMessage(text);
    }
  }, [isConnected, wsConnection, sendMessage]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (wsConnection) {
        wsConnection.close();
      }
    };
  }, [wsConnection]);

  return {
    connect: connectToChatKit,
    disconnect: disconnectFromChatKit,
    sendMessage: sendMessageToChatKit,
    messages,
    isConnected,
    isLoading,
    error
  };
};
'''

    def _generate_generic_component(self, component_name: str, props: Dict[str, Any]) -> str:
        """Generate a generic component."""
        return f'''import React from 'react';

const {component_name} = ({props}) => {{
  return (
    <div className="{component_name.toLowerCase()}">
      <h2>{component_name} Component</h2>
      <p>This is a generated {component_name} component for ChatKit integration.</p>
    </div>
  );
}};

export default {component_name};
'''

    def _generate_generic_hook(self, hook_name: str, config: Dict[str, Any]) -> str:
        """Generate a generic hook."""
        return f'''import {{ useState, useEffect }} from 'react';

export const {hook_name} = (config) => {{
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {{
    // Implementation for {hook_name} hook
    console.log('{hook_name} hook initialized with config:', config);
  }}, [config]);

  return {{
    data,
    loading,
    error,
    // Add hook functions here
  }};
}};
'''

    def _generate_chatkit_component_integration(self, config: Dict[str, Any]) -> str:
        """Generate integration code for ChatKit component."""
        return '''// Example integration in App.js or a parent component
import React from 'react';
import { ChatKitProvider } from './components/ChatKitProvider';
import ChatKitUI from './components/ChatKitUI';

const App = () => {
  return (
    <ChatKitProvider config={{ userId: 'user123' }}>
      <div className="App">
        <header className="App-header">
          <h1>My App with ChatKit</h1>
        </header>
        <main>
          <ChatKitUI
            workflowId="default-workflow"
            userId="user123"
            onMessage={(msg) => console.log('New message:', msg)}
            onError={(err) => console.error('ChatKit error:', err)}
          />
        </main>
      </div>
    </ChatKitProvider>
  );
};

export default App;
'''

    def _generate_chatkit_hook_integration(self, config: Dict[str, Any]) -> str:
        """Generate integration code for ChatKit hook."""
        return '''// Example usage of useChatKit hook in a component
import React, { useEffect } from 'react';
import { useChatKit } from '../hooks/useChatKit';

const ChatComponent = ({ sessionId, userId }) => {
  const {
    connect,
    disconnect,
    sendMessage,
    messages,
    isConnected,
    isLoading
  } = useChatKit();

  useEffect(() => {
    // Connect when component mounts
    if (sessionId) {
      connect({ sessionId, userId });
    }

    // Cleanup on unmount
    return () => disconnect();
  }, [sessionId, userId]);

  const handleSend = async (text) => {
    try {
      await sendMessage(text);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  if (isLoading) return <div>Connecting to ChatKit...</div>;

  return (
    <div>
      <div>Status: {isConnected ? 'Connected' : 'Disconnected'}</div>
      <div>
        {messages.map((msg, idx) => (
          <div key={idx}>{msg.text}</div>
        ))}
      </div>
      <button onClick={() => handleSend('Hello from ChatKit!')}>
        Send Test Message
      </button>
    </div>
  );
};

export default ChatComponent;
'''

    def _generate_chatkit_provider_integration(self, config: Dict[str, Any]) -> str:
        """Generate integration code for ChatKit provider."""
        return '''// Wrap your app with ChatKitProvider in index.js or App.js
import React from 'react';
import ReactDOM from 'react-dom';
import { ChatKitProvider } from './components/ChatKitProvider';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <ChatKitProvider config={{
      userId: localStorage.getItem('userId'),
      apiKey: process.env.REACT_APP_CHATKIT_API_KEY
    }}>
      <App />
    </ChatKitProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
'''

    def _generate_generic_integration(self, integration_type: str, config: Dict[str, Any]) -> str:
        """Generate generic integration code."""
        return f'''// Generic {integration_type} integration code
// This would be customized based on specific requirements
console.log('{integration_type} integration initialized with config:', {json.dumps(config)});
'''


# Singleton instance
openai_chatkit_frontend_skills = OpenAIChatKitFrontendSkills()


async def create_chatkit_ui_component(component_name: str, props: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill to create a React component for the ChatKit UI."""
    return await openai_chatkit_frontend_skills.create_chatkit_ui_component(component_name, props)


async def create_chatkit_hook(hook_name: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill to create a React hook for managing ChatKit connections."""
    return await openai_chatkit_frontend_skills.create_chatkit_hook(hook_name, config)


async def create_chatkit_session(workflow_id: str, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill to create a ChatKit session using the backend API."""
    return await openai_chatkit_frontend_skills.create_chatkit_session(workflow_id, user_id, metadata)


async def generate_chatkit_integration_code(integration_type: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill to generate code for integrating ChatKit into the frontend."""
    return await openai_chatkit_frontend_skills.generate_chatkit_integration_code(integration_type, config)


async def write_chatkit_component_to_file(component_name: str, file_path: str, props: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill to write a ChatKit component to a file."""
    return await openai_chatkit_frontend_skills.write_chatkit_component_to_file(component_name, file_path, props)


# Example usage
async def main():
    """Example of using the OpenAI ChatKit Frontend skills."""
    print("Testing OpenAI ChatKit Frontend Skills")
    print("=" * 50)

    # Create the ChatKit UI component
    component_result = await create_chatkit_ui_component("ChatKitUI")
    print(f"ChatKit UI component creation: {len(component_result.get('component_code', ''))} characters")

    # Create the ChatKit hook
    hook_result = await create_chatkit_hook("useChatKit")
    print(f"useChatKit hook creation: {len(hook_result.get('hook_code', ''))} characters")

    # Create the ChatKit provider
    provider_result = await create_chatkit_ui_component("ChatKitProvider")
    print(f"ChatKitProvider component creation: {len(provider_result.get('component_code', ''))} characters")

    # Generate integration code
    integration_result = await generate_chatkit_integration_code("component")
    print(f"Integration code generation: {len(integration_result.get('integration_code', ''))} characters")

    # Create a ChatKit session
    session_result = await create_chatkit_session("test-workflow-123", "test-user-456", {"test": True})
    print(f"ChatKit session creation: {session_result.get('message')}")

    print("\nSkills are ready to create ChatKit frontend components!")


if __name__ == "__main__":
    asyncio.run(main())