import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

// Custom hook to handle authentication state
export const useAuthState = () => {
  const { user, token, loading, isAuthenticated } = useAuth();

  return {
    user,
    token,
    loading,
    isAuthenticated,
    isAuthorized: !!user && !!token,
  };
};

// Custom hook to handle authentication actions
export const useAuthActions = () => {
  const { register, login, logout, getUserProfile } = useAuth();

  return {
    register,
    login,
    logout,
    getUserProfile,
  };
};

// Custom hook to protect routes/components
export const useProtectedResource = (permission = null) => {
  const { isAuthenticated, user, token } = useAuth();
  const [hasPermission, setHasPermission] = useState(false);

  useEffect(() => {
    if (!isAuthenticated || !token) {
      setHasPermission(false);
      return;
    }

    if (!permission) {
      setHasPermission(true);
      return;
    }

    setHasPermission(true);
  }, [isAuthenticated, user, token, permission]);

  return {
    isAuthenticated,
    hasPermission,
    canAccess: isAuthenticated && hasPermission,
  };
};

// Hook to make authenticated API calls to FastAPI backend
export const useApi = () => {
  const { token, API_BASE_URL } = useAuth();

  const authenticatedFetch = async (url, options = {}) => {
    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
    };

    let response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      try {
        const refreshTokenResponse = await fetch(`${API_BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (refreshTokenResponse.ok) {
          const refreshData = await refreshTokenResponse.json();
          const newToken = refreshData.access_token;

          localStorage.setItem('auth-token', newToken);

          const newHeaders = {
            ...options.headers,
            'Authorization': `Bearer ${newToken}`,
          };

          response = await fetch(url, {
            ...options,
            headers: newHeaders,
          });
        }
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
      }
    }

    return response;
  };

  return { authenticatedFetch };
};