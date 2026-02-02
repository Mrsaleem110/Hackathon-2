import React, { useState, useRef, useEffect } from 'react';

const ChatInterface = ({ userId }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Check if userId is available
  const isAuthResolved = userId !== undefined && userId !== null && userId !== '';

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input field when component mounts
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // Function to send message to backend with MCP-compatible response handling
  const sendMessage = async (message) => {
    if (!message.trim()) return;

    // Early return if userId is not available
    if (!userId || userId === '') {
      console.warn('Cannot send message: User ID is not available');

      // Add error message to the chat
      const errorMessage = {
        id: Date.now(),
        role: 'system',
        content: 'Authentication error: User ID is not available. Please refresh the page or log in again.',
        isError: true,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
      return;
    }

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
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
        timestamp: new Date().toISOString()
      };

      // Add the streaming message to the messages list
      setMessages(prev => [...prev, initialAssistantMessage]);

      // Get the auth token from localStorage (as it's more reliable in async context)
      const token = localStorage.getItem('auth-token');

      if (!token) {
        throw new Error('Authentication token is missing. Please log in again.');
      }

      // Send message to backend API
      const baseUrl = import.meta.env.DEV ? import.meta.env.VITE_API_BASE_URL : '';
      const url = baseUrl ? `${baseUrl}/api/${userId}/chat` : `/api/${userId}/chat`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Add the auth token
        },
        body: JSON.stringify({
          message: message,
          conversation_id: conversationId
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

      // Check if response is JSON before parsing
      const contentType = response.headers.get('content-type');
      let data;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // If not JSON, try to read as text to see what was returned
        const text = await response.text();
        console.error('Expected JSON but got:', text);
        throw new Error(`Expected JSON response but got: ${text.substring(0, 100)}...`);
      }

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

      // Focus input field after sending message
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || isStreaming) return;
    sendMessage(inputValue);
  };

  const handleResetConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Handle keydown for accessibility (Escape to clear input)
  const handleKeyDown = (e) => {
    if (e.key === 'Escape' && inputValue) {
      setInputValue('');
    }
  };

  // If auth is not resolved, show loading state
  if (!isAuthResolved) {
    return (
      <div className="chat-interface" role="main" aria-label="Chat interface">
        <div className="chat-header">
          <h2 tabIndex="0">AI Assistant</h2>
        </div>
        <div className="messages-container" aria-live="polite" aria-label="Chat loading state">
          <div className="loading-state" style={{ padding: '20px', textAlign: 'center' }}>
            <p>Verifying authentication...</p>
            <div className="spinner" style={{
              border: '4px solid rgba(0, 0, 0, 0.1)',
              borderTop: '4px solid #3498db',
              borderRadius: '50%',
              width: '30px',
              height: '30px',
              animation: 'spin 1s linear infinite',
              margin: '10px auto'
            }}></div>
            <p>Please wait while we verify your authentication.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-interface" role="main" aria-label="Chat interface">
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

      <div
        className="messages-container"
        aria-live="polite"
        aria-relevant="additions"
        role="log"
        aria-label="Chat messages"
      >
        {messages.length === 0 ? (
          <div className="welcome-message" tabIndex="0">
            <p>Hello! I'm your AI assistant. How can I help you today?</p>
            <ul aria-label="Available commands">
              <li>You can ask me to manage your tasks</li>
              <li>Ask me to add, list, complete, update, or delete tasks</li>
              <li>Or just chat with me about anything!</li>
            </ul>
          </div>
        ) : (
          <div className="messages-list" role="list">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.role} ${message.isError ? 'error' : ''}`}
                role="listitem"
                aria-label={`${message.role} message: ${message.content || (message.isStreaming ? 'Assistant is typing...' : '')}`}
              >
                <div className="message-content">
                  {message.content || (message.isStreaming && (
                    <span className="typing-indicator" aria-label="Assistant is typing">
                      <span aria-hidden="true"></span>
                      <span aria-hidden="true"></span>
                      <span aria-hidden="true"></span>
                    </span>
                  ))}
                </div>
                <div
                  className="message-timestamp"
                  aria-label={`Sent at ${formatTimestamp(message.timestamp)}`}
                >
                  {formatTimestamp(message.timestamp)}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} aria-hidden="true" />
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="input-form"
        role="form"
        aria-label="Message input form"
      >
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message here..."
          disabled={isLoading || isStreaming}
          aria-label="Type your message"
          aria-describedby="send-button"
          autoComplete="off"
          role="textbox"
          aria-multiline="false"
        />
        <button
          id="send-button"
          type="submit"
          disabled={!inputValue.trim() || isLoading || isStreaming}
          aria-label="Send message"
          title="Send message (Press Enter)"
        >
          {isStreaming ? (
            <span aria-label="Sending message..." role="status">
              Sending...
            </span>
          ) : (
            'Send'
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;