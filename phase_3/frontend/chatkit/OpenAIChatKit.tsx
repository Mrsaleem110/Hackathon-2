// frontend/chatkit/OpenAIChatKit.tsx
import React, { useState, useEffect, useRef } from 'react';
import { openaiConfig } from '../config/openaiConfig';

interface OpenAIChatKitProps {
  userId?: string;
  initialMessages?: Array<{ role: string; content: string }>;
  onMessage?: (message: string) => void;
}

const OpenAIChatKit: React.FC<OpenAIChatKitProps> = ({
  userId = 'user',
  initialMessages = [],
  onMessage
}) => {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [configError, setConfigError] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Check if required configuration is available
  useEffect(() => {
    if (!openaiConfig.apiKey && !openaiConfig.domainKey) {
      const errorMsg = 'OpenAI ChatKit is not configured. Please set NEXT_PUBLIC_OPENAI_API_KEY in development or configure domain allowlist for production.';
      console.error(errorMsg);
      setConfigError(errorMsg);
    }
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = { role: 'user', content: inputValue };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare request to OpenAI API
      const requestBody = {
        model: openaiConfig.model,
        messages: newMessages,
        stream: false, // For simplicity in this implementation
      };

      // Determine the correct API URL based on configuration
      let apiUrl = `${openaiConfig.baseUrl}/chat/completions`;
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authentication based on configuration
      if (openaiConfig.domainKey) {
        // For production with domain allowlist
        headers['Authorization'] = `Bearer ${openaiConfig.domainKey}`;
      } else if (openaiConfig.apiKey) {
        // For development with API key
        headers['Authorization'] = `Bearer ${openaiConfig.apiKey}`;
      } else {
        throw new Error('No valid authentication method configured');
      }

      // Call OpenAI API
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage = data.choices[0].message;

      // Add assistant response to chat
      setMessages(prev => [...prev, assistantMessage]);

      // Call the onMessage callback if provided
      if (onMessage && assistantMessage.content) {
        onMessage(assistantMessage.content);
      }
    } catch (error) {
      console.error('Error calling OpenAI API:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (configError) {
    return (
      <div style={{ padding: '20px', color: 'red', maxWidth: '600px' }}>
        <h3>OpenAI ChatKit Configuration Error</h3>
        <p>{configError}</p>
        <p style={{ marginTop: '10px', fontSize: 'smaller', color: 'gray' }}>
          For production deployment, you need to configure the domain allowlist:
          <ol>
            <li>Deploy your frontend to get a production URL</li>
            <li>Add your domain to OpenAI's allowlist at: https://platform.openai.com/settings/organization/security/domain-allowlist</li>
            <li>Set NEXT_PUBLIC_OPENAI_DOMAIN_KEY with the domain key provided</li>
          </ol>
          For local development, set NEXT_PUBLIC_OPENAI_API_KEY in your environment variables.
        </p>
      </div>
    );
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      width: '100%',
      maxWidth: '800px',
      margin: '0 auto',
      border: '1px solid #ccc',
      borderRadius: '8px',
      overflow: 'hidden'
    }}>
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              marginBottom: '15px',
              padding: '10px',
              borderRadius: '8px',
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.role === 'user' ? '#007AFF' : '#f0f0f0',
              color: msg.role === 'user' ? 'white' : 'black',
              maxWidth: '80%'
            }}
          >
            <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
              {msg.role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div>{msg.content}</div>
          </div>
        ))}
        {isLoading && (
          <div
            style={{
              marginBottom: '15px',
              padding: '10px',
              borderRadius: '8px',
              alignSelf: 'flex-start',
              backgroundColor: '#f0f0f0',
              color: 'black',
              maxWidth: '80%'
            }}
          >
            <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>Assistant</div>
            <div>Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        style={{
          padding: '20px',
          borderTop: '1px solid #ccc',
          display: 'flex'
        }}
      >
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            marginRight: '10px'
          }}
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007AFF',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading || !inputValue.trim() ? 'not-allowed' : 'pointer'
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default OpenAIChatKit;