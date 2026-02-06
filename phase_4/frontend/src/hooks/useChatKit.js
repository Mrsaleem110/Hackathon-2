import { useState, useCallback, useEffect } from 'react';
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
