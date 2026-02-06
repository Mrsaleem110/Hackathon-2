import React from 'react';
import { Navigate } from 'react-router-dom';
import { useUserId } from '../contexts/AuthContext';

const ProtectedRoute = ({ children, requiredPermission = null }) => {
  const { hasUserId, isAuthenticated, loading } = useUserId();

  // Don't show loading state here since it's handled at the route level
  if (loading) {
    return children; // Let the parent route handle loading state
  }

  // Check both authentication status and user ID availability
  if (!isAuthenticated || !hasUserId) {
    // Redirect to login page if not authenticated or user ID is not available
    return <Navigate to="/login" replace />;
  }

  // In a real implementation, we would check for specific permissions here
  // For now, we'll just check if the user is authenticated
  if (requiredPermission) {
    // This is where we'd check if the user has the required permission
    // For now, we'll assume all authenticated users have access
  }

  return children;
};

export default ProtectedRoute;