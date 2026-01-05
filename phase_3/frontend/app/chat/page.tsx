"use client";

import React, { useState, useEffect } from 'react';
import StreamChatUI from '../../chatkit/StreamChatUI';

const ChatPageWrapper = () => {
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeUserId = async () => {
      // First try to get the user ID that might have been set by the todo page
      let storedUserId = localStorage.getItem('user_id');

      if (!storedUserId) {
        const token = localStorage.getItem('access_token');
        if (token) {
          try {
            const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
              headers: {
                'Authorization': `Bearer ${token}`,
              },
            });

            if (response.ok) {
              const user = await response.json();
              // Store the authenticated user's ID
              storedUserId = user.id.toString();
              localStorage.setItem('user_id', storedUserId);
            }
          } catch (error) {
            console.error('Error fetching user info:', error);
          }
        }
      }

      // If still no user ID, generate a temporary one
      if (!storedUserId) {
        storedUserId = `user_${Date.now()}`;
        localStorage.setItem('user_id', storedUserId);
      }

      setUserId(storedUserId);
      setLoading(false);
    };

    initializeUserId();
  }, []);

  if (loading || !userId) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div>
      <StreamChatUI userId={userId} />
    </div>
  );
};

export default ChatPageWrapper;
