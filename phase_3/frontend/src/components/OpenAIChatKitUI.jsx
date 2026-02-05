import React, { useState, useEffect } from 'react';
import { useTask } from '../contexts/TaskContext';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const OpenAIChatKitUI = ({ userId, backendUrl }) => {
  const { triggerTaskUpdate } = useTask();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  // Function to send message to backend
  const sendMessage = async (message) => {
    if (!message.trim()) return;

    // Early return if userId is not available
    if (!userId) {
      console.warn('Cannot send message: User ID is not available');

      // Add error message to the chat
      const errorMessage = {
        id: Date.now(),
        role: 'system',
        content: 'Authentication error: User ID is not available. Please refresh the page or log in again.',
        isError: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMessage]);
      return;
    }

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: message,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setIsStreaming(true);

    try {
      // Create an assistant message placeholder for streaming
      const assistantMessageId = Date.now() + 1;
      const initialAssistantMessage = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        isStreaming: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      // Add the streaming message to the messages list
      setMessages(prev => [...prev, initialAssistantMessage]);

      // Get the auth token from localStorage (as it's more reliable in async context)
      const token = localStorage.getItem('auth-token');

      if (!token) {
        throw new Error('Authentication token is missing. Please log in again.');
      }

      // Send message to backend API
      const baseUrl = backendUrl || (import.meta.env.DEV ? import.meta.env.VITE_API_BASE_URL : 'https://hackathon-2-p-3-backend.vercel.app');
      const url = `${baseUrl}/api/${userId}/chat`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Add the auth token
        },
        body: JSON.stringify({
          message: message,
          conversation_id: conversationId,
          user_id: userId  // Explicitly include userId in the payload
        })
      });

      if (!response.ok) {
        // Get the error details from response
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage += `, message: ${errorData.detail || errorData.message || JSON.stringify(errorData)}`;
        } catch (e) {
          // If we can't parse the error response, just use the status
        }
        throw new Error(errorMessage);
      }

      // Handle JSON response (which may contain MCP-compatible format)
      const data = await response.json();

      // Update conversation ID if new conversation was created
      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
      }

      // Handle MCP-compatible response format
      let responseContent = '';

      // Check if response follows MCP format (with content array)
      if (data.response && typeof data.response === 'object' && Array.isArray(data.response.content)) {
        // Handle MCP format: { content: [{ type: 'text', text: '...' }] }
        responseContent = data.response.content
          .filter(item => item.type === 'text')
          .map(item => item.text)
          .join('\n\n');
      } else if (typeof data.response === 'string') {
        // Handle plain string response
        responseContent = data.response;
      } else {
        // Fallback to JSON stringification
        responseContent = JSON.stringify(data.response, null, 2);
      }

      // Check if any tool calls were made that affect tasks
      if (data.tool_calls && data.tool_calls.length > 0) {
        const hasTaskOperations = data.tool_calls.some(call =>
          ['add_task', 'complete_task', 'delete_task', 'update_task', 'list_tasks'].includes(call.name)
        );

        // If task operations were performed, notify all components to refresh tasks
        if (hasTaskOperations) {
          setTimeout(() => {
            triggerTaskUpdate(); // Trigger global task refresh
          }, 1000); // Small delay to ensure DB transaction completes
        }
      }

      // Update the assistant message with the complete response
      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantMessageId
            ? { ...msg, content: responseContent, isStreaming: false }
            : msg
        )
      );
    } catch (error) {
      console.error('Error sending message:', error);

      // Find the assistant message and update it with error
      setMessages(prev =>
        prev.map(msg =>
          msg.id === Date.now() + 1 || msg.isStreaming
            ? {
                ...msg,
                content: 'Sorry, I encountered an error processing your request. Please try again.',
                isError: true,
                isStreaming: false
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
      setIsStreaming(false);
    }
  };

  const handleResetConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="chat-interface" role="main" aria-label="OpenAI ChatKit UI">
      <div className="chat-header">
        <h2 tabIndex="0">AI Assistant</h2>
        <button
          onClick={handleResetConversation}
          className="reset-button"
          aria-label="Reset conversation"
          title="Reset conversation"
        >
          Reset Chat
        </button>
      </div>

      <MessageList
        messages={messages}
        isLoading={isLoading}
      />

      <MessageInput
        value={inputValue}
        onChange={setInputValue}
        onSubmit={sendMessage}
        isLoading={isLoading}
        isStreaming={isStreaming}
      />
    </div>
  );
};

export default OpenAIChatKitUI;