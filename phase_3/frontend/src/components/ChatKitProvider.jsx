import React, { createContext, useContext, useReducer } from 'react';

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
