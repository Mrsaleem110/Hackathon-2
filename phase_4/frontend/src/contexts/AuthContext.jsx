import React, { createContext, useContext, useState, useEffect } from 'react';
import { authClient } from '../config/betterAuthClient'; // This now exports the BetterAuthClient instance
import ApiService from '../services/api';

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
  const [session, setSession] = useState(null); // BetterAuthClient manages session internally
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null); // BetterAuthClient manages token internally

  // Register function using our FastAPI backend
  const register = async (userData) => {
    try {
      console.log('Starting registration with userData:', userData);
      const response = await ApiService.register(userData);

      console.log('Registration response:', response);

      if (response && response.user) {
        setUser(response.user);
        setSession(response.session); // Store session from API response
        setToken(response.access_token); // Store token from API response
        console.log('Registration successful, user set in context:', response.user);

        // Store token in localStorage for persistence
        if (response.access_token) {
          localStorage.setItem('auth-token', response.access_token);
        }

        return { success: true, user: response.user };
      } else {
        console.error('Registration failed with error:', response?.error?.message || 'Unknown registration error');
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

  // Login function using our FastAPI backend
  const login = async (credentials) => {
    try {
      console.log('Starting login with credentials:', credentials);
      const response = await ApiService.login(credentials);

      console.log('Login response:', response);

      if (response && response.user) {
        setUser(response.user);
        setSession(response.session); // Store session from API response
        setToken(response.access_token); // Store token from API response
        console.log('Login successful, user set in context:', response.user);

        // Store token in localStorage for persistence
        if (response.access_token) {
          localStorage.setItem('auth-token', response.access_token);
        }

        return { success: true, user: response.user };
      } else {
        console.error('Login failed with error:', response?.error?.message || 'Unknown login error');
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
      // Clear token from localStorage
      localStorage.removeItem('auth-token');

      setUser(null);
      setSession(null);
      setToken(null);
      console.log('Logout successful, user state cleared');
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local state even if logout fails
      localStorage.removeItem('auth-token');
      setUser(null);
      setSession(null);
      setToken(null);
    }
  };

  // Get user profile (session)
  const getUserProfile = async () => {
    try {
      // Get token from localStorage if available
      const storedToken = localStorage.getItem('auth-token');

      if (!storedToken) {
        console.log('No stored token found.');
        setUser(null);
        setSession(null);
        setToken(null);
        return null;
      }

      const response = await ApiService.getCurrentUser(storedToken);
      if (response && response.id) {
        setUser(response);
        setSession({ user: response, token: storedToken }); // Create a session-like object
        setToken(storedToken);
        console.log('User profile loaded from API:', response);
        return response;
      }
      console.log('No active session found.');
      setUser(null);
      setSession(null);
      setToken(null);
      return null;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // If getting user fails, clear local state
      logout();
      return null;
    }
  };

  // Check authentication status on initial load
  useEffect(() => {
    const initAuth = async () => {
      try {
        // Get token from localStorage if available
        const storedToken = localStorage.getItem('auth-token');

        if (!storedToken) {
          console.log('Initial auth check: no stored token found.');
          setUser(null);
          setSession(null);
          setToken(null);
        } else {
          // Verify the token by getting user profile
          try {
            const response = await ApiService.getCurrentUser(storedToken);
            if (response && response.id) {
              setUser(response);
              setSession({ user: response, token: storedToken }); // Create a session-like object
              setToken(storedToken);
              console.log('Initial auth check: user found.', response);
            } else {
              console.log('Initial auth check: invalid token.');
              setUser(null);
              setSession(null);
              setToken(null);
              localStorage.removeItem('auth-token'); // Remove invalid token
            }
          } catch (error) {
            console.error('Token validation failed:', error);
            setUser(null);
            setSession(null);
            setToken(null);
            localStorage.removeItem('auth-token'); // Remove invalid token
          }
        }
      } catch (error) {
        console.error('Error during initial auth check:', error);
        setUser(null);
        setSession(null);
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
    isAuthenticated: !!user && !!user.id,
    // API_BASE_URL is not directly related to AuthContext, better to get it where needed
    // Removed API_BASE_URL from here
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
