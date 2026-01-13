'use client';

import React, { useRef, useEffect } from 'react';
import { Message } from '@/types';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div
      className="messages-container flex-1 overflow-y-auto p-4 bg-gray-50"
      role="log"
      aria-live="polite"
      aria-label="Chat messages"
    >
      {messages.length === 0 ? (
        <div className="welcome-message text-center py-12" tabIndex={0}>
          <h3 className="text-xl font-medium text-gray-900 mb-4">Welcome to AI Assistant</h3>
          <p className="text-gray-600 mb-6">How can I help you today?</p>
          <div className="bg-blue-50 rounded-lg p-4 max-w-md mx-auto" role="region" aria-labelledby="capabilities-heading">
            <h4 id="capabilities-heading" className="font-medium text-blue-800 mb-2">You can ask me to:</h4>
            <ul className="text-left text-gray-700 space-y-1" role="list">
              <li className="flex items-start" role="listitem">
                <span className="text-blue-500 mr-2" aria-hidden="true">•</span>
                <span>Manage your tasks (add, list, complete, update, delete)</span>
              </li>
              <li className="flex items-start" role="listitem">
                <span className="text-blue-500 mr-2" aria-hidden="true">•</span>
                <span>Answer questions about your projects</span>
              </li>
              <li className="flex items-start" role="listitem">
                <span className="text-blue-500 mr-2" aria-hidden="true">•</span>
                <span>Provide explanations and suggestions</span>
              </li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="messages-list space-y-4" role="list">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message p-4 rounded-lg max-w-3xl ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white ml-auto'
                  : `bg-white border ${message.isError ? 'border-red-200' : 'border-gray-200'}`
              }`}
              role="listitem"
              aria-labelledby={`message-${message.id}-content`}
              aria-details={`message-${message.id}-timestamp`}
            >
              <div
                id={`message-${message.id}-content`}
                className="message-content"
              >
                {message.content || (message.isStreaming && (
                  <span className="typing-indicator flex items-center" aria-label="Assistant is typing">
                    <span className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-bounce" style={{ animationDelay: '0ms' }} aria-hidden="true"></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-bounce" style={{ animationDelay: '150ms' }} aria-hidden="true"></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} aria-hidden="true"></span>
                  </span>
                ))}
              </div>
              {message.timestamp && (
                <div
                  id={`message-${message.id}-timestamp`}
                  className={`message-timestamp text-xs mt-2 ${
                    message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                  }`}
                  aria-label={`Sent at ${message.timestamp}`}
                >
                  {message.timestamp}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="message p-4 rounded-lg max-w-3xl bg-white border border-gray-200" role="status" aria-live="assertive">
              <div className="message-content">
                <span className="typing-indicator flex items-center" aria-label="Assistant is typing">
                  <span className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-bounce" style={{ animationDelay: '0ms' }} aria-hidden="true"></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full mr-1 animate-bounce" style={{ animationDelay: '150ms' }} aria-hidden="true"></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} aria-hidden="true"></span>
                </span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} aria-hidden="true" />
        </div>
      )}
    </div>
  );
};

export default MessageList;