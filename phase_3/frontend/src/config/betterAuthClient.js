// FastAPI backend API client (replacing Better Auth for Vercel deployment)
const apiBaseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

// API wrapper for FastAPI auth endpoints
const betterAuthAPI = {
  async signUpEmail({ email, password, name }) {
    const response = await fetch(`${apiBaseURL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name, // FastAPI backend expects name field in registration
      }),
    });

    try {
      const data = await response.json();
      if (response.ok) {
        // Store token in localStorage for API requests
        if (data.access_token) {
          localStorage.setItem('auth-token', data.access_token);
        }
        return data;
      } else {
        return { error: data.detail || data.message || 'Registration failed' };
      }
    } catch (e) {
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async signInEmail({ email, password }) {
    const response = await fetch(`${apiBaseURL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    try {
      const data = await response.json();
      if (response.ok) {
        // Store token in localStorage for API requests
        if (data.access_token) {
          localStorage.setItem('auth-token', data.access_token);
        }
        return data;
      } else {
        return { error: data.detail || data.message || 'Login failed' };
      }
    } catch (e) {
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async getSession() {
    const token = localStorage.getItem('auth-token');
    if (!token) {
      return null;
    }

    const response = await fetch(`${apiBaseURL}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.ok) {
      try {
        const data = await response.json();
        return {
          user: data,
          session: { token }
        };
      } catch (e) {
        return null;
      }
    } else {
      // Remove invalid token
      localStorage.removeItem('auth-token');
      return null;
    }
  },

  async signOut() {
    // Just remove the token from localStorage
    localStorage.removeItem('auth-token');
    return true;
  }
};

export { betterAuthAPI as authClient, apiBaseURL };