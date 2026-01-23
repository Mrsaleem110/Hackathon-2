// Better Auth API client for Express server
const betterAuthBaseURL = import.meta.env.VITE_BETTER_AUTH_URL ||
  (typeof window !== 'undefined' && window.location.origin) ||
  'http://localhost:3000';

// API wrapper for Better Auth endpoints
const betterAuthAPI = {
  async signUpEmail({ email, password, name }) {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-up/email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name,
        callbackURL: `${betterAuthBaseURL}/dashboard` // Adjust as needed
      }),
    });

    const data = await response.json();
    return response.ok ? data : { error: data };
  },

  async signInEmail({ email, password }) {
    const response = await fetch(`${betterAuthBaseURL}/api/auth/sign-in/email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    return response.ok ? data : { error: data };
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
      return null;
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