import OpenAI from 'openai';
import { Message } from '@/types';

// Initialize OpenAI client
let openai: OpenAI;

if (process.env.NEXT_PUBLIC_OPENAI_API_KEY) {
  openai = new OpenAI({
    apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY, // This is the default and can be omitted
    dangerouslyAllowBrowser: true // Only for development/testing purposes
  });
} else {
  console.warn('NEXT_PUBLIC_OPENAI_API_KEY is not set. OpenAI integration will not work.');
}

/**
 * Stream messages from OpenAI API
 * @param messages - Array of messages to send to the API
 * @param onChunk - Callback function to handle each chunk of streamed response
 * @param onError - Callback function to handle errors
 */
export const streamOpenAIMessages = async (
  messages: Message[],
  onChunk: (chunk: string) => void,
  onError: (error: Error) => void
): Promise<void> => {
  if (!openai) {
    onError(new Error('OpenAI API key not configured'));
    return;
  }

  try {
    const formattedMessages = messages.map(msg => ({
      role: msg.role as 'user' | 'assistant',
      content: msg.content
    }));

    const stream = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo', // You can change this to gpt-4 if preferred
      messages: formattedMessages,
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      if (content) {
        onChunk(content);
      }
    }
  } catch (error) {
    console.error('Error streaming from OpenAI:', error);
    onError(error instanceof Error ? error : new Error('Unknown error occurred'));
  }
};

/**
 * Send a message to OpenAI API and return the complete response
 * @param messages - Array of messages to send to the API
 * @returns The complete response from OpenAI
 */
export const sendOpenAIMessage = async (messages: Message[]): Promise<string> => {
  if (!openai) {
    throw new Error('OpenAI API key not configured');
  }

  try {
    const formattedMessages = messages.map(msg => ({
      role: msg.role as 'user' | 'assistant',
      content: msg.content
    }));

    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo', // You can change this to gpt-4 if preferred
      messages: formattedMessages,
    });

    return completion.choices[0]?.message?.content || '';
  } catch (error) {
    console.error('Error sending message to OpenAI:', error);
    throw error;
  }
};