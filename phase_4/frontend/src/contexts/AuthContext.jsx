import React, { createContext, useContext, useState, useEffect } from 'react';
import { authClient } from '../config/betterAuthClient'; // This now exports the BetterAuthClient instance

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

  // Register function using Better Auth Client
  const register = async (userData) => {
    try {
      console.log('Starting registration with userData:', userData);
      const response = await authClient.signUpEmail({
        email: userData.email,
        password: userData.password,
        name: userData.name,
      });

      console.log('Registration response:', response);

      if (response && response.user) {
        setUser(response.user);
        setSession(response.session); // Assuming BetterAuthClient returns session on successful registration
        setToken(response.session?.token); // Store token from session if available
        console.log('Registration successful, user set in context:', response.user);
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

  // Login function using Better Auth Client
  const login = async (credentials) => {
    try {
      console.log('Starting login with credentials:', credentials);
      const response = await authClient.signInEmail({
        email: credentials.email,
        password: credentials.password,
      });

      console.log('Login response:', response);

      if (response && response.user) {
        setUser(response.user);
        setSession(response.session); // Assuming BetterAuthClient returns session on successful login
        setToken(response.session?.token); // Store token from session if available
        console.log('Login successful, user set in context:', response.user);
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
      await authClient.signOut(); // BetterAuthClient handles clearing its internal state and localStorage
      setUser(null);
      setSession(null);
      setToken(null);
      console.log('Logout successful, user state cleared');
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local state even if logout fails
      setUser(null);
      setSession(null);
      setToken(null);
    }
  };

  // Get user profile (session)
  const getUserProfile = async () => {
    try {
      const response = await authClient.getSession(); // BetterAuthClient gets session from its internal storage
      if (response && response.user) {
        setUser(response.user);
        setSession(response.session);
        setToken(response.session?.token);
        console.log('User profile loaded from session:', response.user);
        return response.user;
      }
      console.log('No active session found.');
      setUser(null);
      setSession(null);
      setToken(null);
      return null;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // If getSession fails, it means no valid session, so log out
      logout();
      return null;
    }
  };

  // Check authentication status on initial load
  useEffect(() => {
    const initAuth = async () => {
      try {
        const response = await authClient.getSession(); // Get current session from BetterAuthClient
        if (response && response.user) {
          setUser(response.user);
          setSession(response.session);
          setToken(response.session?.token);
          console.log('Initial auth check: user found.', response.user);
        } else {
          console.log('Initial auth check: no active session.');
          setUser(null);
          setSession(null);
          setToken(null);
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
