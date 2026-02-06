'use client';

import React, { useRef, KeyboardEvent } from 'react';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (value: string) => void;
  isLoading: boolean;
  isStreaming: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({
  value,
  onChange,
  onSubmit,
  isLoading,
  isStreaming
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!value.trim() || isLoading || isStreaming) return;
    onSubmit(value);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!value.trim() || isLoading || isStreaming) return;
      onSubmit(value);
    } else if (e.key === 'Escape' && value) {
      onChange('');
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="input-form p-4 bg-white border-t border-gray-200"
      role="form"
      aria-label="Message input form"
    >
      <div className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => handleKeyDown(e as any)}
          placeholder="Type your message here..."
          disabled={isLoading || isStreaming}
          aria-label="Type your message"
          aria-describedby="send-button"
          aria-required="true"
          autoComplete="off"
          className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
          role="textbox"
          aria-multiline={false}
        />
        <button
          id="send-button"
          type="submit"
          disabled={!value.trim() || isLoading || isStreaming}
          aria-label="Send message"
          title="Send message (Press Enter)"
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          aria-busy={isStreaming}
        >
          {isStreaming ? (
            <span aria-live="polite" aria-label="Sending message...">
              Sending...
            </span>
          ) : (
            'Send'
          )}
        </button>
      </div>
    </form>
  );
};

export default MessageInput;