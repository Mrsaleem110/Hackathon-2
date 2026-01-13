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
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

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

      const data = await response.json();

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
      return { success: false, error: error.message };
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

      const data = await response.json();

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
      return { success: false, error: error.message };
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
        // If token is invalid, logout user
        logout();
        return null;
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      return null;
    }
  };

  // Refresh token
  const refreshToken = async () => {
    if (!token) {
      return false;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('auth-token', data.access_token);
        setToken(data.access_token);
        return true;
      } else {
        logout();
        return false;
      }
    } catch (error) {
      console.error('Error refreshing token:', error);
      logout();
      return false;
    }
  };

  // Check authentication status on initial load
  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        const userProfile = await getUserProfile();
        if (!userProfile) {
          // Token was invalid, so clear it
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
    refreshToken,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};