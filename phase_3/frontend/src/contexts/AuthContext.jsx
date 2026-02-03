import React, { createContext, useContext, useState, useEffect } from 'react';
import { authClient } from '../config/betterAuthClient';

export const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Custom hook to specifically check if user ID is available
export const useUserId = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useUserId must be used within an AuthProvider');
  }
  return {
    userId: context.user?.id,
    hasUserId: !!context.user?.id,
    isAuthenticated: context.isAuthenticated,
    loading: context.loading
  };
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  // API base URL for FastAPI backend (for tasks, not auth)
  // Use absolute URLs for production to avoid issues with Vercel rewrites and CORS
  const isDevelopment = import.meta.env.DEV;
  const API_BASE_URL = isDevelopment
    ? (import.meta.env.VITE_API_BASE_URL || process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001')
    : (import.meta.env.VITE_API_BASE_URL || 'https://hackathon-2-p-3-backend.vercel.app');

  // Register function using Better Auth
  const register = async (userData) => {
    try {
      console.log('Starting registration with userData:', userData); // Debug log
      const response = await authClient.signUpEmail({
        email: userData.email,
        password: userData.password,
        name: userData.name,
      });

      console.log('Registration response:', response); // Debug log

      if (response && !response.error) {
        // Successfully registered
        console.log('Setting user in context:', response.user); // Debug log
        setUser(response.user);
        setSession(response.session);

        // Get token from response session or from localStorage if it's been set there
        let tokenToSet = null;
        if (response.session?.token) {
          tokenToSet = response.session.token;
        } else {
          // Check if token was already stored in localStorage by the authClient
          tokenToSet = localStorage.getItem('auth-token');
        }

        // CRITICAL: Ensure we always have a token by double-checking localStorage after registration
        if (!tokenToSet) {
          tokenToSet = localStorage.getItem('auth-token');
        }

        if (tokenToSet) {
          // Ensure token is in localStorage (double-check)
          localStorage.setItem('auth-token', tokenToSet);
          setToken(tokenToSet);
          console.log('Token set in context:', tokenToSet.substring(0, 10) + '...'); // Debug log
        } else {
          console.error('No token found to set in context after registration'); // Critical debug log
          // Try to get any token that might exist in localStorage with different naming
          const allKeys = Object.keys(localStorage);
          for (const key of allKeys) {
            if (key.toLowerCase().includes('token')) {
              const potentialToken = localStorage.getItem(key);
              if (potentialToken && typeof potentialToken === 'string' && potentialToken.includes('.')) {
                const parts = potentialToken.split('.');
                if (parts.length === 3) { // JWT format
                  console.log(`Found potential token in localStorage key: ${key}`);
                  localStorage.setItem('auth-token', potentialToken);
                  setToken(potentialToken);
                  tokenToSet = potentialToken;
                  break;
                }
              }
            }
          }

          if (!tokenToSet) {
            console.error('Still no token found after checking all localStorage keys');
          }
        }

        console.log('Registration successful, user set in context:', response.user); // Debug log
        return { success: true, user: response.user };
      } else {
        console.error('Registration failed with error:', response?.error?.message); // Debug log
        return { success: false, error: response?.error?.message || 'Registration failed' };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        error: error.message || 'Registration failed'
      };
    }
  };

  // Login function using Better Auth
  const login = async (credentials) => {
    try {
      console.log('Starting login with credentials:', credentials); // Debug log
      const response = await authClient.signInEmail({
        email: credentials.email,
        password: credentials.password,
      });

      console.log('Login response:', response); // Debug log

      if (response && !response.error) {
        // Successfully logged in
        console.log('Setting user in context during login:', response.user); // Debug log
        setUser(response.user);
        setSession(response.session);

        // Get token from response session or from localStorage if it's been set there
        let tokenToSet = null;
        if (response.session?.token) {
          tokenToSet = response.session.token;
        } else {
          // Check if token was already stored in localStorage by the authClient
          tokenToSet = localStorage.getItem('auth-token');
        }

        // CRITICAL: Ensure we always have a token by double-checking localStorage after login
        if (!tokenToSet) {
          tokenToSet = localStorage.getItem('auth-token');
        }

        if (tokenToSet) {
          // Ensure token is in localStorage (double-check)
          localStorage.setItem('auth-token', tokenToSet);
          setToken(tokenToSet);
          console.log('Token set in context:', tokenToSet.substring(0, 10) + '...'); // Debug log
        } else {
          console.error('No token found to set in context after login'); // Critical debug log
          // Try to get any token that might exist in localStorage with different naming
          const allKeys = Object.keys(localStorage);
          for (const key of allKeys) {
            if (key.toLowerCase().includes('token')) {
              const potentialToken = localStorage.getItem(key);
              if (potentialToken && typeof potentialToken === 'string' && potentialToken.includes('.')) {
                const parts = potentialToken.split('.');
                if (parts.length === 3) { // JWT format
                  console.log(`Found potential token in localStorage key: ${key}`);
                  localStorage.setItem('auth-token', potentialToken);
                  setToken(potentialToken);
                  tokenToSet = potentialToken;
                  break;
                }
              }
            }
          }

          if (!tokenToSet) {
            console.error('Still no token found after checking all localStorage keys');
          }
        }

        console.log('Login successful, user set in context:', response.user); // Debug log
        return { success: true, user: response.user };
      } else {
        console.error('Login failed with error:', response?.error?.message); // Debug log
        return { success: false, error: response?.error?.message || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        error: error.message || 'Login failed'
      };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authClient.signOut();
      localStorage.removeItem('auth-token');
      setToken(null);
      setUser(null);
      setSession(null);
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local state even if logout fails
      localStorage.removeItem('auth-token');
      setToken(null);
      setUser(null);
      setSession(null);
    }
  };

  // Get user profile
  const getUserProfile = async () => {
    try {
      const response = await authClient.getSession();
      if (response && response.session) {
        setUser(response.user);
        setSession(response.session);

        // Get token from response session or from localStorage if it's been set there
        let tokenToSet = null;
        if (response.session?.token) {
          tokenToSet = response.session.token;
        } else {
          // Check if token was already stored in localStorage by the authClient
          tokenToSet = localStorage.getItem('auth-token');
        }

        // CRITICAL: Ensure we always have a token by double-checking localStorage after session retrieval
        if (!tokenToSet) {
          tokenToSet = localStorage.getItem('auth-token');
        }

        if (tokenToSet) {
          // Ensure token is in localStorage (double-check)
          localStorage.setItem('auth-token', tokenToSet);
          setToken(tokenToSet);
          console.log('Token set in context from getUserProfile:', tokenToSet.substring(0, 10) + '...'); // Debug log
        } else {
          console.warn('No token found in localStorage during getUserProfile'); // Debug log
          // Try to get any token that might exist in localStorage with different naming
          const allKeys = Object.keys(localStorage);
          for (const key of allKeys) {
            if (key.toLowerCase().includes('token')) {
              const potentialToken = localStorage.getItem(key);
              if (potentialToken && typeof potentialToken === 'string' && potentialToken.includes('.')) {
                const parts = potentialToken.split('.');
                if (parts.length === 3) { // JWT format
                  console.log(`Found potential token in localStorage key: ${key}`);
                  localStorage.setItem('auth-token', potentialToken);
                  setToken(potentialToken);
                  tokenToSet = potentialToken;
                  break;
                }
              }
            }
          }
        }

        return response.user;
      }
      return null;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      logout();
      return null;
    }
  };

  // Check authentication status on initial load
  useEffect(() => {
    const initAuth = async () => {
      try {
        // Get the current session from Better Auth
        const sessionResponse = await authClient.getSession();

        if (sessionResponse && sessionResponse.session) {
          setUser(sessionResponse.user);
          setSession(sessionResponse.session);

          // Get token from response session or from localStorage if it's been set there
          let tokenToSet = null;
          if (sessionResponse.session?.token) {
            tokenToSet = sessionResponse.session.token;
          } else {
            // Check if token was already stored in localStorage by the authClient
            tokenToSet = localStorage.getItem('auth-token');
          }

          // CRITICAL: Ensure we always have a token by double-checking localStorage after session retrieval
          if (!tokenToSet) {
            tokenToSet = localStorage.getItem('auth-token');
          }

          if (tokenToSet) {
            // Ensure token is in localStorage (double-check)
            localStorage.setItem('auth-token', tokenToSet);
            setToken(tokenToSet);
            console.log('Token set in context from init:', tokenToSet.substring(0, 10) + '...'); // Debug log
          } else {
            console.warn('No token found in localStorage during init'); // Debug log
            // Try to get any token that might exist in localStorage with different naming
            const allKeys = Object.keys(localStorage);
            for (const key of allKeys) {
              if (key.toLowerCase().includes('token')) {
                const potentialToken = localStorage.getItem(key);
                if (potentialToken && typeof potentialToken === 'string' && potentialToken.includes('.')) {
                  const parts = potentialToken.split('.');
                  if (parts.length === 3) { // JWT format
                    console.log(`Found potential token in localStorage key: ${key}`);
                    localStorage.setItem('auth-token', potentialToken);
                    setToken(potentialToken);
                    tokenToSet = potentialToken;
                    break;
                  }
                }
              }
            }
          }
        } else {
          // No session found, clear storage
          localStorage.removeItem('auth-token');
          setToken(null);
          console.log('No session found, cleared auth token'); // Debug log
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        localStorage.removeItem('auth-token');
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const value = {
    user,
    session,
    token,
    loading,
    register,
    login,
    logout,
    getUserProfile,
    isAuthenticated: !!user && !!user.id, // Require user.id to be present for authentication
    API_BASE_URL, // Export for use in API calls
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};