// This file configures the Better Auth client to talk to better_auth_server.js
// However, we're now using our custom auth endpoints, so we can simplify this

// Export the API base URL for our custom FastAPI backend
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

// Placeholder authClient to avoid breaking existing imports - will be replaced with API service
export const authClient = {
  signUpEmail: async (userData) => {
    // This will be handled by our custom API service
    console.warn('Using authClient.signUpEmail - this should be handled by our API service instead');
    return { error: { message: 'Direct BetterAuth client not configured for this setup' } };
  },
  signInEmail: async (credentials) => {
    // This will be handled by our custom API service
    console.warn('Using authClient.signInEmail - this should be handled by our API service instead');
    return { error: { message: 'Direct BetterAuth client not configured for this setup' } };
  },
  signOut: async () => {
    // This will be handled by our custom API service
    console.warn('Using authClient.signOut - this should be handled by our custom API service instead');
    return {};
  },
  getSession: async () => {
    // This will be handled by our custom API service
    console.warn('Using authClient.getSession - this should be handled by our API service instead');
    return {};
  }
};
