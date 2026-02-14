// This file configures the Better Auth client to talk to better_auth_server.js

import { createAuthClient } from 'better-auth/react';

// Use VITE_AUTH_BASE_URL for the Better Auth service
// Fallback to http://localhost:3001 for local development if VITE_AUTH_BASE_URL is not set
const authServiceBaseUrl = import.meta.env.VITE_AUTH_BASE_URL || 'http://localhost:3001';

// Initialize the Better Auth client
const authClient = createAuthClient({
  baseURL: authServiceBaseUrl,
  // Add other necessary configurations for Better Auth client if needed
  // e.g., redirectUrl for OAuth flows if applicable
});

// Export the initialized Better Auth client
export { authClient };

// You might still need a separate API client for your FastAPI backend (tasks, chat, etc.)
// This would typically go in a different file or be a separate export.
// For now, I'll keep the FastAPI related base URL for reference if needed elsewhere.
export const FASTAPI_API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';


// SINGLE SOURCE OF TRUTH FOR USER ID (this part can remain similar)
export function resolveUserId(session) {
  if (!session) return null;

  const user = session.user;

  if (!user || typeof user !== 'object') return null;

  return (
    user.id ||
    user.user_id ||
    user.userId ||
    user.sub ||
    null
  );
}
