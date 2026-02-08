import React from 'react';
import { ChatKitProvider } from './ChatKitProvider';
import ChatKitUI from './ChatKitUI';

const ChatKitExample = () => {
  const handleNewMessage = (message) => {
    console.log('New message sent:', message);
  };

  const handleError = (error) => {
    console.error('ChatKit error:', error);
  };

  return (
    <div className="chatkit-example">
      <h1>OpenAI ChatKit UI Example</h1>
      <p>This is an example of the ChatKit UI integrated into a React application.</p>

      <div className="chat-container">
        <ChatKitProvider config={{ userId: 'example-user-123' }}>
          <ChatKitUI
            workflowId="example-workflow"
            userId="example-user-123"
            onMessage={handleNewMessage}
            onError={handleError}
            className="embedded-chatkit"
          />
        </ChatKitProvider>
      </div>
    </div>
  );
};

export default ChatKitExample;