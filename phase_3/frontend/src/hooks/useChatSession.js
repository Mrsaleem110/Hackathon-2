import { useState, useCallback } from 'react';

const useChatSession = () => {
  const [sessionData, setSessionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const createSession = useCallback(async (userId, workflowId) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/chatkit/session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId,
          workflowId
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to create session: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setSessionData(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const refreshSession = useCallback(async (sessionId) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/chatkit/session/${sessionId}/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to refresh session: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setSessionData(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    sessionData,
    isLoading,
    error,
    createSession,
    refreshSession,
  };
};

export default useChatSession;