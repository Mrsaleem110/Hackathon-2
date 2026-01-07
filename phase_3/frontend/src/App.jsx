import React, { useState, useEffect } from 'react';
import { useChatkit } from '@openai/chatkit';
import './App.css';

const App = () => {
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  // Use ChatKit for chat functionality
  const {
    connectToChatkit,
    sendMessage,
    messages: chatkitMessages,
    isConnecting,
    isConnected
  } = useChatkit();

  useEffect(() => {
    // Connect to ChatKit on component mount
    connectToChatkit({
      instanceLocator: process.env.VITE_CHATKIT_INSTANCE_LOCATOR,
      token: process.env.VITE_CHATKIT_TOKEN,
      userId: 'todo-user',
    });
  }, []);

  // Update local messages when ChatKit messages change
  useEffect(() => {
    if (chatkitMessages) {
      setMessages(chatkitMessages);
    }
  }, [chatkitMessages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim() || isLoading || !isConnected) return;

    try {
      setIsLoading(true);

      // Send message via ChatKit
      await sendMessage({
        text: userInput,
      });

      setUserInput('');
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <div className="header">
          <h1>AI Todo Assistant</h1>
          <p>Manage your tasks with natural language</p>
        </div>

        <div className="chat-messages">
          {isConnecting && (
            <div className="message assistant-message">
              <div className="message-content">Connecting to chat...</div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.senderId === 'todo-user' ? 'user-message' : 'assistant-message'}`}
            >
              <div className="message-content">
                {message.text}
              </div>
              <div className="message-role">
                {message.senderId === 'todo-user' ? 'You' : message.senderId}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message assistant-message">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your message here (e.g., 'Add a task to buy groceries')..."
            disabled={isLoading || !isConnected}
          />
          <button type="submit" disabled={isLoading || !isConnected}>
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;