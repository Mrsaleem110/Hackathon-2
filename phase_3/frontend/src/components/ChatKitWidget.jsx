import React, { useState, useEffect } from 'react';
import { ChatKitProvider, ChatInterface } from '@openai/chatkit-react';

const ChatKitWidget = ({ workflowId, userId }) => {
  const [sessionToken, setSessionToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to fetch session token from backend
  const fetchSessionToken = async () => {
    try {
      const response = await fetch('/api/chatkit/session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId: userId || 'anonymous',
          workflowId: workflowId
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create session');
      }

      const data = await response.json();
      setSessionToken(data.session_token);
      setIsLoading(false);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSessionToken();
  }, [workflowId, userId]);

  if (isLoading) {
    return (
      <div className="chatkit-loading">
        <p>Loading chat...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chatkit-error">
        <p>Error: {error}</p>
        <button onClick={fetchSessionToken}>Retry</button>
      </div>
    );
  }

  return (
    <div className="chatkit-container">
      {sessionToken && (
        <ChatKitProvider
          token={sessionToken}
          workflowId={workflowId}
        >
          <ChatInterface />
        </ChatKitProvider>
      )}
    </div>
  );
};

export default ChatKitWidget;