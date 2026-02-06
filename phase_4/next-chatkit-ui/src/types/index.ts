export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  isStreaming?: boolean;
  isError?: boolean;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls?: any[];
}