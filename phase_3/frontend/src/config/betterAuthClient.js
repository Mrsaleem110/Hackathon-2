// FastAPI Auth API client (replacing Better Auth with custom JWT auth)
// Use relative paths in development to leverage Vite proxy, absolute URLs in development when explicitly configured
const isDevelopment = import.meta.env.DEV;

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
    console.log('Making registration request to:', url); // Debug log

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

    console.log('Registration response status:', response.status); // Debug log

    try {
      const data = await response.json();
      console.log('Registration response data:', data); // Debug log

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
        console.error('Registration failed:', errorMessage); // Debug log
        return {
          error: {
            message: typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage)
          }
        };
      }
    } catch (e) {
      console.error('Registration error parsing response:', e); // Debug log
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async signInEmail({ email, password }) {
    const url = apiBaseURL ? `${apiBaseURL}/auth/login` : '/auth/login';
    console.log('Making login request to:', url); // Debug log

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

    console.log('Login response status:', response.status); // Debug log

    try {
      const data = await response.json();
      console.log('Login response data:', data); // Debug log

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
        console.error('Login failed:', errorMessage); // Debug log
        return {
          error: {
            message: typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage)
          }
        };
      }
    } catch (e) {
      console.error('Login error parsing response:', e); // Debug log
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async getSession() {
    const token = localStorage.getItem('auth-token');
    if (!token) {
      console.log('No auth token found in localStorage'); // Debug log
      return null;
    }

    console.log('Getting session with token'); // Debug log
    const url = apiBaseURL ? `${apiBaseURL}/auth/me` : '/auth/me';
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    console.log('Session response status:', response.status); // Debug log

    if (response.ok) {
      try {
        const data = await response.json();
        console.log('Session response data:', data); // Debug log
        // Return proper format expected by AuthContext
        return {
          user: data,
          session: {
            token: token,
            tokenType: 'bearer'
          }
        };
      } catch (e) {
        console.error('Error parsing session response:', e); // Debug log
        return null;
      }
    } else {
      console.error('Session request failed, removing token'); // Debug log
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