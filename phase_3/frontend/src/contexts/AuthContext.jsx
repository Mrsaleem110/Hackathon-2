import React, { createContext, useContext, useState, useEffect } from 'react';

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
  const [token, setToken] = useState(localStorage.getItem('auth-token') || null);
  const [loading, setLoading] = useState(true);

  // API base URL
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

  // Register function
  const register = async (userData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      let data;
      try {
        data = await response.json();
      } catch (jsonError) {
        // If JSON parsing fails, create a generic error response
        return {
          success: false,
          error: `Non-JSON response received. Status: ${response.status}`
        };
      }

      if (response.ok) {
        // Store token in localStorage
        localStorage.setItem('auth-token', data.access_token);
        setToken(data.access_token);
        setUser(data.user);
        return { success: true, user: data.user };
      } else {
        return { success: false, error: data.detail || 'Registration failed' };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: error.message || 'Network error occurred during registration' };
    }
  };

  // Login function
  const login = async (credentials) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      let data;
      try {
        data = await response.json();
      } catch (jsonError) {
        // If JSON parsing fails, create a generic error response
        return {
          success: false,
          error: `Non-JSON response received. Status: ${response.status}`
        };
      }

      if (response.ok) {
        // Store token in localStorage
        localStorage.setItem('auth-token', data.access_token);
        setToken(data.access_token);
        setUser(data.user);
        return { success: true, user: data.user };
      } else {
        return { success: false, error: data.detail || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message || 'Network error occurred during login' };
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('auth-token');
    setToken(null);
    setUser(null);
  };

  // Get user profile
  const getUserProfile = async () => {
    if (!token) {
      return null;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        return userData;
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Failed to fetch user profile:', response.status, errorData);
        // If token is invalid, logout user
        logout();
        return null;
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // If there's a network error, the token might be invalid
      logout();
      return null;
    }
  };

  // Check authentication status on initial load
  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        try {
          const userProfile = await getUserProfile();
          if (!userProfile) {
            // Token was invalid, so clear it
            localStorage.removeItem('auth-token');
            setToken(null);
          }
        } catch (error) {
          console.error('Error initializing auth:', error);
          // If there's an error getting the user profile, clear the token
          localStorage.removeItem('auth-token');
          setToken(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const value = {
    user,
    token,
    loading,
    register,
    login,
    logout,
    getUserProfile,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};