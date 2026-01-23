import { createAuthClient } from "@better-auth/client";

// Better Auth client configuration
const betterAuthBaseURL = import.meta.env.VITE_BETTER_AUTH_URL ||
  (typeof window !== 'undefined' && window.location.origin) ||
  'http://localhost:3000';

export const authClient = createAuthClient({
  baseURL: betterAuthBaseURL,
});

export { betterAuthBaseURL };