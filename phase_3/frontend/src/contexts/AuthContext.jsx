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

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  // API base URL for FastAPI backend (for tasks, not auth)
  // Use relative paths in production to leverage Vercel rewrites, absolute URLs in development
  const isDevelopment = import.meta.env.DEV;
  const API_BASE_URL = isDevelopment
    ? (import.meta.env.VITE_API_BASE_URL || process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001')
    : ''; // Use relative paths in production to leverage Vercel rewrites

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
        // For Better Auth with cookies, the token is typically stored in cookies
        // We'll use the session data to get the token if available
        if (response.session?.token) {
          localStorage.setItem('auth-token', response.session.token);
          setToken(response.session.token);
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
        if (response.session?.token) {
          localStorage.setItem('auth-token', response.session.token);
          setToken(response.session.token);
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
        if (response.session?.token) {
          localStorage.setItem('auth-token', response.session.token);
          setToken(response.session.token);
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

          // Store token for API requests to FastAPI backend
          if (sessionResponse.session?.token) {
            localStorage.setItem('auth-token', sessionResponse.session.token);
            setToken(sessionResponse.session.token);
          }
        } else {
          // No session found, clear storage
          localStorage.removeItem('auth-token');
          setToken(null);
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
    isAuthenticated: !!user,
    API_BASE_URL, // Export for use in API calls
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};