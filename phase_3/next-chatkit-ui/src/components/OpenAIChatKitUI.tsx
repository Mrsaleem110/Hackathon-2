'use client';

import React, { useState, useEffect } from 'react';
import MessageList from '@/components/MessageList';
import MessageInput from '@/components\MessageInput';
import { Message } from '@/types';
import { streamOpenAIMessages, sendOpenAIMessage } from '@/services/openai-service';

interface OpenAIChatKitUIProps {
  userId: string;
  backendUrl?: string;
}

const OpenAIChatKitUI: React.FC<OpenAIChatKitUIProps> = ({ userId, backendUrl }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  // Function to send message to OpenAI API with streaming
  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
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
      const assistantMessageId = (Date.now() + 1).toString();
      const initialAssistantMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        isStreaming: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      // Add the streaming message to the messages list
      setMessages(prev => [...prev, initialAssistantMessage]);

      // Prepare messages for API call (include conversation history)
      const messagesForAPI = [...messages, userMessage];

      // Use streaming API to get response
      let fullResponse = '';

      await streamOpenAIMessages(
        messagesForAPI,
        (chunk) => {
          // Update the assistant message with the new chunk
          fullResponse += chunk;

          setMessages(prev =>
            prev.map(msg =>
              msg.id === assistantMessageId
                ? { ...msg, content: fullResponse }
                : msg
            )
          );
        },
        (error) => {
          throw error;
        }
      );

      // Update the assistant message with the complete response and remove streaming flag
      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantMessageId
            ? { ...msg, content: fullResponse, isStreaming: false }
            : msg
        )
      );
    } catch (error) {
      console.error('Error sending message:', error);

      // Find the assistant message and update it with error
      setMessages(prev =>
        prev.map(msg =>
          msg.id === (Date.now() + 1).toString() || msg.isStreaming
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
    <div
      className="chat-interface bg-white rounded-lg shadow-md overflow-hidden flex flex-col h-full border border-gray-200"
      role="region"
      aria-label="Chat interface"
    >
      <div className="chat-header bg-blue-600 text-white p-4 flex justify-between items-center" role="banner">
        <h2 className="text-xl font-semibold" tabIndex={0}>AI Assistant</h2>
        <button
          onClick={handleResetConversation}
          className="bg-white text-blue-600 hover:bg-blue-50 px-3 py-1 rounded-md text-sm font-medium transition-colors"
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