import React, { useState, useRef, useEffect } from 'react';

const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="messages-container" role="log" aria-live="polite">
      {messages.length === 0 ? (
        <div className="welcome-message" tabIndex="0">
          <p>Hello! I'm your AI assistant. How can I help you today?</p>
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
              {message.timestamp && (
                <div
                  className="message-timestamp"
                  aria-label={`Sent at ${message.timestamp}`}
                >
                  {message.timestamp}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="message assistant loading" role="status">
              <div className="message-content">
                <span className="typing-indicator" aria-label="Assistant is typing">
                  <span aria-hidden="true"></span>
                  <span aria-hidden="true"></span>
                  <span aria-hidden="true"></span>
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