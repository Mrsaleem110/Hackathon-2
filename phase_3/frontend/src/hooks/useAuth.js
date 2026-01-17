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
    // Check if user is authenticated
    if (!isAuthenticated || !token) {
      setHasPermission(false);
      return;
    }

    // If no specific permission is required, just check authentication
    if (!permission) {
      setHasPermission(true);
      return;
    }

    // In a real implementation, we would check user permissions
    // For now, we'll assume all authenticated users have basic permissions
    setHasPermission(true);
  }, [isAuthenticated, user, token, permission]);

  return {
    isAuthenticated,
    hasPermission,
    canAccess: isAuthenticated && hasPermission,
  };
};

// Hook to make authenticated API calls
export const useApi = () => {
  const { token } = useAuth();

  const authenticatedFetch = async (url, options = {}) => {
    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
    };

    let response = await fetch(url, {
      ...options,
      headers,
    });

    // If token expired, try to refresh it (if refresh endpoint exists)
    if (response.status === 401) {
      try {
        // Attempt to refresh the token
        const refreshTokenResponse = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (refreshTokenResponse.ok) {
          const refreshData = await refreshTokenResponse.json();
          const newToken = refreshData.access_token;

          // Update token in localStorage and context
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
        // If refresh fails, the original 401 response is returned
      }
    }

    return response;
  };

  return { authenticatedFetch };
};