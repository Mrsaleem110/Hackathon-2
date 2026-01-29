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
      const rawData = await response.json();
      console.log('Raw registration response data:', rawData); // Debug log
      console.log('Raw registration response type:', typeof rawData); // Debug log
      console.log('Is raw registration response an array?', Array.isArray(rawData)); // Debug log

      // Handle the response properly - it might be an array
      let data = rawData;
      if (Array.isArray(rawData)) {
        console.log('Registration response is an array with length:', rawData.length); // Debug log
        console.log('Registration array elements:', rawData); // Debug log
        // If it's an array, we need to determine which element contains the auth data
        // Usually it's the first element, but let's check both
        for (let i = 0; i < rawData.length; i++) {
          console.log(`Registration array element ${i}:`, rawData[i], typeof rawData[i]); // Debug log
        }
        // Take the first element that looks like it contains auth data
        data = rawData.find(item => item && typeof item === 'object' && (item.access_token || item.token || item.user));
        if (!data && rawData.length > 0) {
          data = rawData[0]; // Fallback to first element
        }
      }

      console.log('Processed registration response data:', data); // Debug log

      if (response.ok) {
        // Determine the correct token field - it might be in different places
        let tokenToStore = null;
        if (data && data.access_token) {
          tokenToStore = data.access_token;
        } else if (data && data.token) {
          tokenToStore = data.token;
        } else if (data && data.session && data.session.token) {
          tokenToStore = data.session.token;
        }

        // Store token in localStorage for API requests
        if (tokenToStore) {
          localStorage.setItem('auth-token', tokenToStore);
          console.log('Token stored in localStorage:', tokenToStore.substring(0, 10) + '...'); // Debug log
        } else {
          console.error('No token found in response to store:', data, rawData); // Debug log
        }

        // Return proper format expected by AuthContext
        // The user property might be in a different field
        let userData = null;
        if (data && data.user) {
          userData = data.user;
        } else if (data && data.data && data.data.user) {
          userData = data.data.user;
        } else if (data && data.data && !data.user) {
          userData = data.data;
        } else {
          userData = data;
        }

        return {
          user: userData,
          session: {
            token: tokenToStore || (data && data.access_token) || (data && data.token) || (data && data.session && data.session.token),
            tokenType: (data && data.token_type) || 'bearer'
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
      const rawData = await response.json();
      console.log('Raw login response data:', rawData); // Debug log
      console.log('Raw login response type:', typeof rawData); // Debug log
      console.log('Is raw response an array?', Array.isArray(rawData)); // Debug log

      // Handle the response properly - it might be an array
      let data = rawData;
      if (Array.isArray(rawData)) {
        console.log('Response is an array with length:', rawData.length); // Debug log
        console.log('Array elements:', rawData); // Debug log
        // If it's an array, we need to determine which element contains the auth data
        // Usually it's the first element, but let's check both
        for (let i = 0; i < rawData.length; i++) {
          console.log(`Array element ${i}:`, rawData[i], typeof rawData[i]); // Debug log
        }
        // Take the first element that looks like it contains auth data
        data = rawData.find(item => item && typeof item === 'object' && (item.access_token || item.token || item.user));
        if (!data && rawData.length > 0) {
          data = rawData[0]; // Fallback to first element
        }
      }

      console.log('Processed login response data:', data); // Debug log

      if (response.ok) {
        // Determine the correct token field - it might be in different places
        let tokenToStore = null;
        if (data && data.access_token) {
          tokenToStore = data.access_token;
        } else if (data && data.token) {
          tokenToStore = data.token;
        } else if (data && data.session && data.session.token) {
          tokenToStore = data.session.token;
        }

        // Store token in localStorage for API requests
        if (tokenToStore) {
          localStorage.setItem('auth-token', tokenToStore);
          console.log('Token stored in localStorage:', tokenToStore.substring(0, 10) + '...'); // Debug log
        } else {
          console.error('No token found in response to store:', data, rawData); // Debug log
        }

        // Return proper format expected by AuthContext
        // The user property might be in a different field
        let userData = null;
        if (data && data.user) {
          userData = data.user;
        } else if (data && data.data && data.data.user) {
          userData = data.data.user;
        } else if (data && data.data && !data.user) {
          userData = data.data;
        } else {
          userData = data;
        }

        return {
          user: userData,
          session: {
            token: tokenToStore || (data && data.access_token) || (data && data.token) || (data && data.session && data.session.token),
            tokenType: (data && data.token_type) || 'bearer'
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

        // Check the actual structure of the response
        console.log('Session response structure:', Object.keys(data || {})); // Debug log

        // Return proper format expected by AuthContext
        // The user property might be in a different field
        let userData = null;
        if (data.user) {
          userData = data.user;
        } else if (data.data && data.data.user) {
          userData = data.data.user;
        } else if (data.data && !data.user) {
          userData = data.data;
        } else if (Array.isArray(data) && data.length > 0) {
          // If response is an array, use the first element as user data if it's not the token
          userData = data[0];
        } else {
          userData = data;
        }

        return {
          user: userData,
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