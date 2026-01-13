import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ children, requiredPermission = null }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect to login page if not authenticated
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