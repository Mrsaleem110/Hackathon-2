import { useState, useCallback } from 'react';

const useChatSession = () => {
  const [sessionData, setSessionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const createSession = useCallback(async (userId, workflowId) => {
    setIsLoading(true);
    setError(null);

    try {
      const baseUrl = import.meta.env.DEV ? (import.meta.env.VITE_API_BASE_URL || '') : 'https://hackathon-2-p-3-backend.vercel.app';
      const url = baseUrl ? `${baseUrl}/api/chatkit/session` : '/api/chatkit/session';
      const response = await fetch(url, {
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
      const baseUrl = import.meta.env.DEV ? (import.meta.env.VITE_API_BASE_URL || '') : 'https://hackathon-2-p-3-backend.vercel.app';
      const url = baseUrl ? `${baseUrl}/api/chatkit/session/${sessionId}/refresh` : `/api/chatkit/session/${sessionId}/refresh`;
      const response = await fetch(url, {
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