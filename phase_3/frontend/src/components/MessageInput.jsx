import React, { useRef } from 'react';

const MessageInput = ({ value, onChange, onSubmit, isLoading, isStreaming }) => {
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim() || isLoading || isStreaming) return;
    onSubmit(value);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    } else if (e.key === 'Escape' && value) {
      onChange('');
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="input-form"
      role="form"
      aria-label="Message input form"
    >
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message here..."
        disabled={isLoading || isStreaming}
        aria-label="Type your message"
        aria-describedby="send-button"
        autoComplete="off"
        role="textbox"
        aria-multiline="false"
      />
      <button
        id="send-button"
        type="submit"
        disabled={!value.trim() || isLoading || isStreaming}
        aria-label="Send message"
        title="Send message (Press Enter)"
      >
        {isStreaming ? (
          <span aria-label="Sending message..." role="status">
            Sending...
          </span>
        ) : (
          'Send'
        )}
      </button>
    </form>
  );
};

export default MessageInput;