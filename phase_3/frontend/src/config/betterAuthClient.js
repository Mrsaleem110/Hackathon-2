// FastAPI Auth API client (replacing Better Auth with custom JWT auth)
// Use relative paths in development to leverage Vite proxy, absolute URLs in development when explicitly configured
const isDevelopment = import.meta.env.DEV;
const apiBaseURL = isDevelopment
  ? (import.meta.env.VITE_API_BASE_URL || '') // Use env var if set, otherwise relative path for Vite proxy
  : (import.meta.env.VITE_API_BASE_URL || ''); // Use env var in production, fallback to relative paths

// Fallback to a default backend URL if none is provided in production
const getApiBaseUrl = () => {
  if (isDevelopment) {
    return import.meta.env.VITE_API_BASE_URL || '';
  } else {
    // In production, use the environment variable or fall back to the deployed backend
    return import.meta.env.VITE_API_BASE_URL || 'https://hackathon-2-p-3-backend.vercel.app';
  }
};

const apiBaseURL = getApiBaseUrl();

// API wrapper for FastAPI auth endpoints
const betterAuthAPI = {
  async signUpEmail({ email, password, name }) {
    const url = apiBaseURL ? `${apiBaseURL}/auth/register` : '/auth/register';
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name, // FastAPI auth expects name field in registration
      }),
    });

    try {
      const data = await response.json();
      if (response.ok) {
        // Store token in localStorage for API requests
        if (data.access_token) {
          localStorage.setItem('auth-token', data.access_token);
        }
        // Return proper format expected by AuthContext
        return {
          user: data.user,
          session: {
            token: data.access_token,
            tokenType: data.token_type
          }
        };
      } else {
        const errorMessage = data.detail || 'Registration failed';
        return {
          error: {
            message: typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage)
          }
        };
      }
    } catch (e) {
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async signInEmail({ email, password }) {
    const url = apiBaseURL ? `${apiBaseURL}/auth/login` : '/auth/login';
    const response = await fetch(url, {
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
        // Return proper format expected by AuthContext
        return {
          user: data.user,
          session: {
            token: data.access_token,
            tokenType: data.token_type
          }
        };
      } else {
        const errorMessage = data.detail || 'Login failed';
        return {
          error: {
            message: typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage)
          }
        };
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

    const url = apiBaseURL ? `${apiBaseURL}/auth/me` : '/auth/me';
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.ok) {
      try {
        const data = await response.json();
        // Return proper format expected by AuthContext
        return {
          user: data,
          session: {
            token: token,
            tokenType: 'bearer'
          }
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

export { betterAuthAPI as authClient };