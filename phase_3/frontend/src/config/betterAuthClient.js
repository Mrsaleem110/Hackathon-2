// Better Auth API client for Express server
const betterAuthBaseURL = import.meta.env.VITE_BETTER_AUTH_URL ||
  (typeof window !== 'undefined' && window.location.origin) ||
  'http://localhost:3000';

// API wrapper for Better Auth endpoints
const betterAuthAPI = {
  async signUpEmail({ email, password, name }) {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-up`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name,
        // Remove callbackURL from the body - it's usually passed as a query param if needed
      }),
    });

    // Check if response is ok before parsing JSON
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      // Try to parse error response, but handle if it's not JSON
      try {
        const errorData = await response.json();
        return { error: errorData };
      } catch (e) {
        // If response is not JSON, return a generic error
        return { error: { message: `HTTP ${response.status}: ${response.statusText}` } };
      }
    }
  },

  async signInEmail({ email, password }) {
    // Better Auth expects a POST request to /api/auth/sign-in with email and password
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-in/email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    // Check if response is ok before parsing JSON
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      // Try to parse error response, but handle if it's not JSON
      try {
        const errorData = await response.json();
        return { error: errorData };
      } catch (e) {
        // If response is not JSON, return a generic error
        return { error: { message: `HTTP ${response.status}: ${response.statusText}` } };
      }
    }
  },

  async getSession() {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/session`, {
      method: 'GET',
      credentials: 'include', // Important for cookies
    });

    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      // Handle non-OK responses gracefully
      if (response.status === 401) {
        // No session exists
        return null;
      }
      // Try to parse error response
      try {
        const errorData = await response.json();
        console.error('Session error:', errorData);
        return null;
      } catch (e) {
        // If response is not JSON, return null
        return null;
      }
    }
  },

  async signOut() {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-out`, {
      method: 'POST',
      credentials: 'include', // Important for cookies
    });

    return response.ok;
  }
};

export { betterAuthAPI as authClient, betterAuthBaseURL };