// FastAPI Auth API client (replacing Better Auth with custom JWT auth)
// Use direct backend URL for auth endpoints to avoid CORS issues with Vercel rewrites
const isDevelopment = import.meta.env.DEV;

// Use direct backend URL for auth endpoints to ensure proper CORS handling
const getDirectAuthBaseUrl = () => {
  if (isDevelopment) {
    if (import.meta.env.VITE_DOCKER_DEV === 'true') {
      return 'http://backend:8000'; // Direct to backend service in Docker Compose (where our auth routes are)
    }
    return 'http://localhost:8000'; // Point to backend port where our auth routes are located
  } else {
    // In production, always use the direct backend URL for auth endpoints
    return import.meta.env.VITE_API_BASE_URL || 'https://hackathon-2-p-3-backend.vercel.app';
  }
};

const authApiBaseURL = getDirectAuthBaseUrl();

// API wrapper for FastAPI auth endpoints - using direct backend URL
const betterAuthAPI = {
  async signUpEmail({ email, password, name }) {
    const url = `${authApiBaseURL}/auth/register`;
    console.log('Making registration request to:', url); // Debug log
    console.log('Auth API Base URL:', authApiBaseURL); // Debug log

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

        // Additional check: if data is a direct object with access_token at root
        if (!tokenToStore && typeof data === 'object' && data !== null) {
          // Check if access_token is directly in the response object
          const keys = Object.keys(data);
          for (const key of keys) {
            if (key.toLowerCase().includes('token') && typeof data[key] === 'string') {
              if (key.toLowerCase() === 'access_token' || key.toLowerCase() === 'token') {
                tokenToStore = data[key];
                break;
              }
            }
          }
        }

        // Store token in localStorage for API requests - CRITICAL FIX
        if (tokenToStore) {
          // Check if the token looks like an error message instead of a proper JWT
          // JWT tokens have 3 parts separated by dots, while error messages typically don't
          const tokenParts = tokenToStore.split('.');
          if (tokenParts.length === 3 && tokenParts[0].length > 0 && tokenParts[1].length > 0 && tokenParts[2].length > 0) {
            // This looks like a proper JWT token
            localStorage.setItem('auth-token', tokenToStore);
            console.log('Token stored in localStorage:', tokenToStore.substring(0, 10) + '...'); // Debug log
          } else {
            // This looks like an error message, not a JWT token
            console.error('Received error message instead of token:', tokenToStore);
            console.error('Full response data:', data, rawData);
            tokenToStore = null; // Don't store error messages as tokens
          }
        } else {
          console.error('No token found in response to store:', data, rawData); // Debug log

          // Try to find any string field that might be a token by checking for JWT-like patterns
          if (data && typeof data === 'object') {
            for (const [key, value] of Object.entries(data)) {
              if (typeof value === 'string' && value.includes('.')) { // JWT tokens have dots
                const parts = value.split('.');
                if (parts.length === 3) { // JWT has 3 parts separated by dots
                  // Double-check that this looks like a proper JWT and not an error message
                  if (parts[0].length > 0 && parts[1].length > 0 && parts[2].length > 0) {
                    tokenToStore = value;
                    console.log('Found potential JWT token in field:', key);
                    localStorage.setItem('auth-token', tokenToStore);
                    break;
                  }
                }
              }
            }
          }

          // If still no token, try to extract from response structure based on known backend format
          if (!tokenToStore) {
            // Backend returns {access_token: "...", token_type: "...", user: {...}}
            if (rawData && rawData.access_token) {
              const rawToken = rawData.access_token;
              const rawTokenParts = rawToken.split('.');
              if (rawTokenParts.length === 3 && rawTokenParts[0].length > 0 && rawTokenParts[1].length > 0 && rawTokenParts[2].length > 0) {
                // This looks like a proper JWT token
                tokenToStore = rawToken;
                localStorage.setItem('auth-token', tokenToStore);
                console.log('Extracted token from rawData:', tokenToStore.substring(0, 10) + '...');
              } else {
                console.error('Raw data contained error message instead of token:', rawToken);
              }
            }
          }
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

        // Ensure token is in the session response
        const sessionWithToken = {
          token: tokenToStore || (data && data.access_token) || (data && data.token) || (data && data.session && data.session.token),
          tokenType: (data && data.token_type) || 'bearer'
        };

        console.log('Final session object:', sessionWithToken); // Debug log

        return {
          user: userData,
          session: sessionWithToken
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
      // Even if parsing fails, try to read the raw response text to see what's happening
      try {
        const textResponse = await response.text();
        console.error('Raw response text:', textResponse);
      } catch (textError) {
        console.error('Could not read raw response:', textError);
      }
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async signInEmail({ email, password }) {
    const url = `${authApiBaseURL}/auth/login`;
    console.log('Making login request to:', url); // Debug log
    console.log('Auth API Base URL:', authApiBaseURL); // Debug log

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

        // Additional check: if data is a direct object with access_token at root
        if (!tokenToStore && typeof data === 'object' && data !== null) {
          // Check if access_token is directly in the response object
          const keys = Object.keys(data);
          for (const key of keys) {
            if (key.toLowerCase().includes('token') && typeof data[key] === 'string') {
              if (key.toLowerCase() === 'access_token' || key.toLowerCase() === 'token') {
                tokenToStore = data[key];
                break;
              }
            }
          }
        }

        // Store token in localStorage for API requests - CRITICAL FIX
        if (tokenToStore) {
          // Check if the token looks like an error message instead of a proper JWT
          // JWT tokens have 3 parts separated by dots, while error messages typically don't
          const tokenParts = tokenToStore.split('.');
          if (tokenParts.length === 3 && tokenParts[0].length > 0 && tokenParts[1].length > 0 && tokenParts[2].length > 0) {
            // This looks like a proper JWT token
            localStorage.setItem('auth-token', tokenToStore);
            console.log('Token stored in localStorage:', tokenToStore.substring(0, 10) + '...'); // Debug log
          } else {
            // This looks like an error message, not a JWT token
            console.error('Received error message instead of token:', tokenToStore);
            console.error('Full response data:', data, rawData);
            tokenToStore = null; // Don't store error messages as tokens
          }
        } else {
          console.error('No token found in response to store:', data, rawData); // Debug log

          // Try to find any string field that might be a token by checking for JWT-like patterns
          if (data && typeof data === 'object') {
            for (const [key, value] of Object.entries(data)) {
              if (typeof value === 'string' && value.includes('.')) { // JWT tokens have dots
                const parts = value.split('.');
                if (parts.length === 3) { // JWT has 3 parts separated by dots
                  // Double-check that this looks like a proper JWT and not an error message
                  if (parts[0].length > 0 && parts[1].length > 0 && parts[2].length > 0) {
                    tokenToStore = value;
                    console.log('Found potential JWT token in field:', key);
                    localStorage.setItem('auth-token', tokenToStore);
                    break;
                  }
                }
              }
            }
          }

          // If still no token, try to extract from response structure based on known backend format
          if (!tokenToStore) {
            // Backend returns {access_token: "...", token_type: "...", user: {...}}
            if (rawData && rawData.access_token) {
              const rawToken = rawData.access_token;
              const rawTokenParts = rawToken.split('.');
              if (rawTokenParts.length === 3 && rawTokenParts[0].length > 0 && rawTokenParts[1].length > 0 && rawTokenParts[2].length > 0) {
                // This looks like a proper JWT token
                tokenToStore = rawToken;
                localStorage.setItem('auth-token', tokenToStore);
                console.log('Extracted token from rawData:', tokenToStore.substring(0, 10) + '...');
              } else {
                console.error('Raw data contained error message instead of token:', rawToken);
              }
            }
          }
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

        // Ensure token is in the session response
        const sessionWithToken = {
          token: tokenToStore || (data && data.access_token) || (data && data.token) || (data && data.session && data.session.token),
          tokenType: (data && data.token_type) || 'bearer'
        };

        console.log('Final session object:', sessionWithToken); // Debug log

        return {
          user: userData,
          session: sessionWithToken
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
      // Even if parsing fails, try to read the raw response text to see what's happening
      try {
        const textResponse = await response.text();
        console.error('Raw response text:', textResponse);
      } catch (textError) {
        console.error('Could not read raw response:', textError);
      }
      return { error: { message: `Failed to parse JSON response: ${e.message}` } };
    }
  },

  async getSession() {
    const token = localStorage.getItem('auth-token');
    console.log('Getting session - token exists:', !!token); // Debug log

    if (!token) {
      console.log('No auth token found in localStorage'); // Debug log
      return null;
    }

    // First, validate that the token looks like a proper JWT before using it
    const tokenParts = token.split('.');
    if (tokenParts.length !== 3 || tokenParts[0].length === 0 || tokenParts[1].length === 0 || tokenParts[2].length === 0) {
      console.error('Invalid token format detected, removing from storage:', token); // Debug log
      localStorage.removeItem('auth-token');
      return null;
    }

    console.log('Getting session with token'); // Debug log
    const url = `${authApiBaseURL}/auth/me`;
    console.log('Session URL:', url); // Debug log

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });

      console.log('Session response status:', response.status); // Debug log

      if (response.ok) {
        const data = await response.json();
        console.log('Session response data:', data); // Debug log

        // Check the actual structure of the response
        console.log('Session response structure:', Object.keys(data || {})); // Debug log

        // Check if the response contains an error message instead of user data
        if (data && typeof data === 'object' && (data.error || data.detail || data.message)) {
          console.error('Session response contains error:', data.error || data.detail || data.message); // Debug log
          // Remove invalid token
          localStorage.removeItem('auth-token');
          return null;
        }

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
      } else {
        // If the session request fails, the token might be invalid/expired
        console.error('Session request failed, removing token'); // Debug log
        const errorText = await response.text();
        console.error('Session error response:', errorText); // Debug log

        // Remove invalid token
        localStorage.removeItem('auth-token');
        return null;
      }
    } catch (error) {
      console.error('Network error getting session:', error); // Debug log
      return null;
    }
  },

  async signOut() {
    // Remove the token from localStorage
    localStorage.removeItem('auth-token');

    // Also clear any related auth data that might be stored
    localStorage.removeItem('better-auth.session_token');
    localStorage.removeItem('better-auth.expires');

    return true;
  }
};

export { betterAuthAPI as authClient };
// 🔑 SINGLE SOURCE OF TRUTH FOR USER ID
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
