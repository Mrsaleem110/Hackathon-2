
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import OpenAIChatKitUI from './components/OpenAIChatKitUI';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
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
              <Dashboard />
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
              <Dashboard />
            </ProtectedRoute>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
    </Routes>
  );
};

// Dashboard component that contains the chat UI
const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="app">
      <header className="app-header">
        <h1>Welcome, {user?.name || user?.email || 'User'}!</h1>
      </header>
      <div className="chat-container">
        <OpenAIChatKitUI userId={user?.id} />
      </div>
    </div>
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