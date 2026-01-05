import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Paper, Typography, List, ListItem, ListItemText, CircularProgress, Alert } from '@mui/material';
import { io, Socket } from 'socket.io-client';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ChatProps {
  userId: string;
}

const SocketChatUI: React.FC<ChatProps> = ({ userId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [socket, setSocket] = useState<Socket | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000', {
      transports: ['websocket', 'polling'],
    });

    setSocket(newSocket);

    // Listen for incoming messages
    newSocket.on('chat_message', (data) => {
      const message: Message = {
        id: `msg-${Date.now()}-${Math.random()}`,
        role: 'assistant',
        content: data.content,
        timestamp: data.timestamp || new Date().toISOString(),
      };
      setMessages(prev => [...prev, message]);
      setLoading(false);
    });

    // Listen for errors
    newSocket.on('error', (data) => {
      setError(data.message || 'An error occurred');
      setLoading(false);
    });

    // Load conversation history
    newSocket.emit('load_history', { userId });

    // Listen for history response
    newSocket.on('history_loaded', (data) => {
      setMessages(data.messages || []);
    });

    // Cleanup on unmount
    return () => {
      newSocket.disconnect();
    };
  }, [userId]);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = () => {
    if (!inputValue.trim() || !socket) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setError(null);
    setLoading(true);

    // Send message via socket
    socket.emit('send_message', {
      userId,
      message: inputValue,
      timestamp: new Date().toISOString()
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', p: 2 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Todo AI Chat (Socket.io)
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper
        elevation={3}
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          mb: 2,
          overflow: 'hidden'
        }}
      >
        <Box sx={{ flex: 1, overflowY: 'auto', p: 2 }}>
          <List>
            {messages.map((message) => (
              <ListItem
                key={message.id}
                sx={{
                  justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                  mb: 1,
                }}
              >
                <Box
                  sx={{
                    maxWidth: '70%',
                    p: 1.5,
                    borderRadius: 2,
                    backgroundColor: message.role === 'user' ? '#e3f2fd' : '#f5f5f5',
                    alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
                  }}
                >
                  <ListItemText
                    primary={message.content}
                    primaryTypographyProps={{ variant: 'body1' }}
                  />
                  <Typography
                    variant="caption"
                    color="textSecondary"
                    sx={{ display: 'block', textAlign: 'right', mt: 0.5 }}
                  >
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </Typography>
                </Box>
              </ListItem>
            ))}
            {loading && (
              <ListItem sx={{ justifyContent: 'center' }}>
                <CircularProgress size={24} />
              </ListItem>
            )}
            <div ref={messagesEndRef} />
          </List>
        </Box>
      </Paper>

      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          multiline
          rows={2}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
          variant="outlined"
          disabled={loading}
        />
        <Button
          variant="contained"
          onClick={handleSendMessage}
          disabled={loading || !inputValue.trim()}
          sx={{ height: 'fit-content' }}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default SocketChatUI;