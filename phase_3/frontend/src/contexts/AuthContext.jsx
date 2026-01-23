import React, { createContext, useContext, useState, useEffect } from 'react';
import { authClient } from '../config/betterAuthClient';

const AuthContext = createContext();

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
  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    process.env.REACT_APP_API_BASE_URL ||
    'http://localhost:8001';

  // Register function using Better Auth
  const register = async (userData) => {
    try {
      const response = await authClient.signUp.email({
        email: userData.email,
        password: userData.password,
        name: userData.name,
        image: userData.image,
      }, {
        onSuccess: (ctx) => {
          // Successfully registered
          setUser(ctx.data.user);
          setSession(ctx.data.session);
          if (ctx.data.session?.token) {
            localStorage.setItem('auth-token', ctx.data.session.token);
            setToken(ctx.data.session.token);
          }
        },
        onError: (ctx) => {
          console.error('Registration error:', ctx.error);
        }
      });

      return { success: true, user: response?.user };
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
      const response = await authClient.signIn.email({
        email: credentials.email,
        password: credentials.password,
      }, {
        onSuccess: (ctx) => {
          // Successfully logged in
          setUser(ctx.data.user);
          setSession(ctx.data.session);
          if (ctx.data.session?.token) {
            localStorage.setItem('auth-token', ctx.data.session.token);
            setToken(ctx.data.session.token);
          }
        },
        onError: (ctx) => {
          console.error('Login error:', ctx.error);
        }
      });

      return { success: true, user: response?.user };
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
      if (response && response.data) {
        setUser(response.data.user);
        setSession(response.data.session);
        return response.data.user;
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

        if (sessionResponse && sessionResponse.data) {
          const { user: sessionUser, session: sessionData } = sessionResponse.data;
          setUser(sessionUser);
          setSession(sessionData);

          // Store token for API requests to FastAPI backend
          if (sessionData?.token) {
            localStorage.setItem('auth-token', sessionData.token);
            setToken(sessionData.token);
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