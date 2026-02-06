'use client';

import React from 'react';
import OpenAIChatKitUI from '@/components/OpenAIChatKitUI';

const ChatPage = () => {
  // Using a demo user ID - in a real app, this would come from authentication
  const userId = 'demo-user';

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm py-4 px-6 border-b" role="banner">
        <h1 className="text-2xl font-bold text-gray-900" tabIndex={0}>AI Assistant</h1>
      </header>
      <main className="flex-1 flex flex-col items-center justify-center p-4" role="main">
        <div className="w-full max-w-4xl h-[calc(100vh-150px)] flex flex-col">
          <OpenAIChatKitUI userId={userId} />
        </div>
      </main>
    </div>
  );
};

export default ChatPage;