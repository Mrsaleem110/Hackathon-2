// Better Auth API client
// Use relative paths in production to leverage Vercel rewrites, absolute URLs in development
const isDevelopment = import.meta.env.DEV;
const apiBaseURL = isDevelopment
  ? (import.meta.env.VITE_API_BASE_URL || 'http://localhost:9000') // Better Auth server runs on port 9000
  : ''; // Use relative paths in production to leverage Vercel rewrites

// API wrapper for Better Auth endpoints
const betterAuthAPI = {
  async signUpEmail({ email, password, name }) {
    const url = apiBaseURL ? `${apiBaseURL}/api/auth/sign-up` : '/api/auth/sign-up';
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name, // Better Auth expects name field in registration
      }),
    });

    try {
      const data = await response.json();
      if (response.ok) {
        // Store token in localStorage for API requests
        if (data.token) {
          localStorage.setItem('auth-token', data.token);
        }
        // Return proper format expected by AuthContext
        return {
          user: data.user,
          session: {
            token: data.token,
            tokenType: 'bearer'
          }
        };
      } else {
        const errorMessage = data.message || 'Registration failed';
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
    const url = apiBaseURL ? `${apiBaseURL}/api/auth/sign-in/email` : '/api/auth/sign-in/email';
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
        if (data.token) {
          localStorage.setItem('auth-token', data.token);
        }
        // Return proper format expected by AuthContext
        return {
          user: data.user,
          session: {
            token: data.token,
            tokenType: 'bearer'
          }
        };
      } else {
        const errorMessage = data.message || 'Login failed';
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

    const url = apiBaseURL ? `${apiBaseURL}/api/auth/session` : '/api/auth/session';
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
          user: data.user,
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