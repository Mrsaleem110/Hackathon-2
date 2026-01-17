
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import OpenAIChatKitUI from './components/OpenAIChatKitUI';
import ChatInterface from './components/ChatInterface';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardLayout from './components/DashboardLayout';
import Dashboard from './components/Dashboard';
import TasksDashboard from './components/TasksDashboard';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import './App.css';

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
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/"
        element={
          user ? (
            <ProtectedRoute>
              <Navigate to="/dashboard" replace />
            </ProtectedRoute>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/dashboard"
        element={
          user ? (
            <ProtectedRoute>
              <DashboardLayout user={user}>
                <Dashboard />
              </DashboardLayout>
            </ProtectedRoute>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/tasks"
        element={
          user ? (
            <ProtectedRoute>
              <DashboardLayout user={user}>
                <TasksDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/analytics"
        element={
          user ? (
            <ProtectedRoute>
              <DashboardLayout user={user}>
                <AnalyticsDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/chat"
        element={
          user ? (
            <ProtectedRoute>
              <DashboardLayout user={user}>
                <ChatInterface userId={user.id} />
              </DashboardLayout>
            </ProtectedRoute>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
    </Routes>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <MainApp />
      </Router>
    </AuthProvider>
  );
};

export default App;