
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { TaskProvider, useTask } from './contexts/TaskContext';
import OpenAIChatKitUI from './components/OpenAIChatKitUI';
import ChatInterface from './components/ChatInterface';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import LandingPage from './pages/LandingPage';
import DashboardLayout from './components/DashboardLayout';
import Dashboard from './components/Dashboard';
import TaskDashboard from './components/TaskDashboard';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import './App.css';

// Component to handle the protected routes
const ProtectedLayout = ({ user, children }) => {
  return (
    <ProtectedRoute>
      <DashboardLayout user={user}>
        {children}
      </DashboardLayout>
    </ProtectedRoute>
  );
};

// Wrapper component for public routes (redirects authenticated users)
const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-container">
        <div>Loading...</div>
      </div>
    );
  }

  return user ? <Navigate to="/dashboard" replace /> : children;
};

// Main App component that handles routing
const MainApp = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="app">
        <div className="loading-container">
          <div>Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      {/* Public routes - accessible when not authenticated */}
      <Route path="/login" element={
        <PublicRoute>
          <LoginPage />
        </PublicRoute>
      } />
      <Route path="/register" element={
        <PublicRoute>
          <RegisterPage />
        </PublicRoute>
      } />

      {/* Public route - landing page accessible to all users */}
      <Route path="/" element={user ? <Navigate to="/dashboard" replace /> : <LandingPage />} />

      {/* Protected routes - only accessible when authenticated */}
      <Route path="/dashboard" element={user ? <ProtectedLayout user={user}><Dashboard /></ProtectedLayout> : <Navigate to="/login" replace />} />
      <Route path="/tasks" element={user ? <ProtectedLayout user={user}><TaskDashboard /></ProtectedLayout> : <Navigate to="/login" replace />} />
      <Route path="/analytics" element={user ? <ProtectedLayout user={user}><AnalyticsDashboard /></ProtectedLayout> : <Navigate to="/login" replace />} />
      <Route path="/chat" element={user && user.id ? <ProtectedLayout user={user}><ChatInterface userId={user.id} /></ProtectedLayout> : <Navigate to="/login" replace />} />

      {/* Public routes - accessible when not authenticated */}
      <Route path="/login" element={
        <PublicRoute>
          <LoginPage />
        </PublicRoute>
      } />
      <Route path="/register" element={
        <PublicRoute>
          <RegisterPage />
        </PublicRoute>
      } />

      {/* Catch-all route for undefined paths - redirect to dashboard if authenticated, home if not */}
      <Route path="*" element={!user ? <Navigate to="/" replace /> : <Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <TaskProvider>
        <Router>
          <MainApp />
        </Router>
      </TaskProvider>
    </AuthProvider>
  );
};

export default App;