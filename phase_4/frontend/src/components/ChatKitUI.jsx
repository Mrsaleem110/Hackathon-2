import React, { useState, useEffect } from 'react';
import { useChatKit } from '../hooks/useChatKit';

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
    const baseUrl = import.meta.env.DEV ? (import.meta.env.VITE_API_BASE_URL || '') : 'https://hackathon-2-p-3-backend.vercel.app';
    if (sessionId) {
      // Retrieve existing session
      const url = baseUrl ? `${baseUrl}/api/chatkit/session/${sessionId}` : `/api/chatkit/session/${sessionId}`;
      return await fetch(url).then(r => r.json());
    } else {
      // Create new session
      const url = baseUrl ? `${baseUrl}/api/chatkit/session` : '/api/chatkit/session';
      return await fetch(url, {
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
