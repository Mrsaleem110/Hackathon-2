// frontend/app/chat/openai/page.tsx
'use client';

import React from 'react';
import OpenAIChatKit from '../../../chatkit/OpenAIChatKit';

const OpenAIChatPage = () => {
  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>OpenAI ChatKit</h1>
      <p>This is an implementation of OpenAI ChatKit with domain allowlist configuration.</p>
      <div style={{ marginTop: '20px' }}>
        <OpenAIChatKit />
      </div>
    </div>
  );
};

export default OpenAIChatPage;