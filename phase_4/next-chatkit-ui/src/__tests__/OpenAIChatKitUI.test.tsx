import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import OpenAIChatKitUI from '@/components/OpenAIChatKitUI';

// Mock the OpenAI service
jest.mock('@/services/openai-service', () => ({
  streamOpenAIMessages: jest.fn(),
}));

describe('OpenAIChatKitUI', () => {
  const mockUserId = 'test-user';

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the chat interface with header and input', () => {
    render(<OpenAIChatKitUI userId={mockUserId} />);

    expect(screen.getByRole('banner')).toBeInTheDocument();
    expect(screen.getByRole('form', { name: /Message input form/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /Type your message/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Send message/i })).toBeInTheDocument();
  });

  it('allows user to type and send a message', async () => {
    render(<OpenAIChatKitUI userId={mockUserId} />);

    const input = screen.getByRole('textbox', { name: /Type your message/i });
    const sendButton = screen.getByRole('button', { name: /Send message/i });

    fireEvent.change(input, { target: { value: 'Hello, AI!' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(input).toHaveValue('');
    });
  });

  it('disables input when loading', () => {
    render(<OpenAIChatKitUI userId={mockUserId} />);

    const input = screen.getByRole('textbox', { name: /Type your message/i });
    const sendButton = screen.getByRole('button', { name: /Send message/i });

    // Simulate loading state
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Input and button should be disabled during loading
    expect(input).toBeDisabled();
    expect(sendButton).toBeDisabled();
  });

  it('resets conversation when reset button is clicked', () => {
    render(<OpenAIChatKitUI userId={mockUserId} />);

    const resetButton = screen.getByRole('button', { name: /Reset conversation/i });
    fireEvent.click(resetButton);

    expect(screen.getByText(/Welcome to AI Assistant/i)).toBeInTheDocument();
  });

  it('shows welcome message when no messages exist', () => {
    render(<OpenAIChatKitUI userId={mockUserId} />);

    expect(screen.getByText(/Welcome to AI Assistant/i)).toBeInTheDocument();
    expect(screen.getByText(/How can I help you today\?/i)).toBeInTheDocument();
  });
});