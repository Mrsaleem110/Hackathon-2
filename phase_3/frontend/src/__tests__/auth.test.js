import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import { ProtectedRoute } from '../components/ProtectedRoute';
import { App } from '../App';

// Mock the better-auth client
jest.mock('../config/betterAuthClient', () => ({
  getSession: jest.fn(),
  signIn: jest.fn(),
  signOut: jest.fn(),
}));

// Mock the ChatInterface component
jest.mock('../components/ChatInterface', () => ({
  ChatInterface: ({ children }) => <div data-testid="chat-interface">{children}</div>,
}));

describe('Authentication Session Resolution Tests', () => {
  // Mock session data
  const mockSessionWithUserId = {
    user: {
      id: 'test-user-id-123',
      email: 'test@example.com',
      name: 'Test User'
    },
    expiresAt: new Date(Date.now() + 3600000).toISOString()
  };

  const mockSessionWithoutUserId = {
    user: {
      email: 'test@example.com',
      name: 'Test User'
      // Missing id field
    },
    expiresAt: new Date(Date.now() + 3600000).toISOString()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('T025: Verify user.id is available before ChatInterface renders', async () => {
    // Mock the session to include user ID
    const { getSession } = require('../config/betterAuthClient');
    getSession.mockResolvedValue(mockSessionWithUserId);

    // Wrap the component in AuthProvider
    const TestComponent = () => {
      const { user, isLoading } = useAuth();

      return (
        <div>
          {isLoading ? (
            <div data-testid="loading">Loading...</div>
          ) : user?.id ? (
            <div data-testid="chat-ready">Chat Interface Ready - UserID: {user.id}</div>
          ) : (
            <div data-testid="no-access">No Access - Missing UserID</div>
          )}
        </div>
      );
    };

    const { getByTestId } = render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Initially should show loading
    expect(getByTestId('loading')).toBeInTheDocument();

    // Wait for auth state to resolve
    await waitFor(() => {
      expect(screen.queryByTestId('loading')).not.toBeInTheDocument();
    }, { timeout: 3000 });

    // Should show chat ready with user ID
    await waitFor(() => {
      const chatReadyElement = screen.getByTestId('chat-ready');
      expect(chatReadyElement).toBeInTheDocument();
      expect(chatReadyElement.textContent).toContain('UserID: test-user-id-123');
    }, { timeout: 3000 });
  });

  test('T025: Handle case when user.id is missing from session', async () => {
    // Mock the session without user ID
    const { getSession } = require('../config/betterAuthClient');
    getSession.mockResolvedValue(mockSessionWithoutUserId);

    const TestComponent = () => {
      const { user, isLoading } = useAuth();

      return (
        <div>
          {isLoading ? (
            <div data-testid="loading">Loading...</div>
          ) : user?.id ? (
            <div data-testid="chat-ready">Chat Interface Ready - UserID: {user.id}</div>
          ) : (
            <div data-testid="no-access">No Access - Missing UserID</div>
          )}
        </div>
      );
    };

    const { getByTestId } = render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Initially should show loading
    expect(getByTestId('loading')).toBeInTheDocument();

    // Wait for auth state to resolve
    await waitFor(() => {
      expect(screen.queryByTestId('loading')).not.toBeInTheDocument();
    }, { timeout: 3000 });

    // Should show no access message when user ID is missing
    await waitFor(() => {
      expect(screen.getByTestId('no-access')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  test('T025: ProtectedRoute waits for complete auth state resolution', async () => {
    const { getSession } = require('../config/betterAuthClient');

    // Initially return a session with user ID
    getSession.mockResolvedValue(mockSessionWithUserId);

    const MockProtectedComponent = () => <div data-testid="protected-content">Protected Content</div>;

    const { queryByTestId } = render(
      <AuthProvider>
        <ProtectedRoute>
          <MockProtectedComponent />
        </ProtectedRoute>
      </AuthProvider>
    );

    // The protected content should eventually appear when auth is resolved
    await waitFor(() => {
      expect(queryByTestId('protected-content')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  test('T025: Auth state resolves correctly with loading states', async () => {
    const { getSession } = require('../config/betterAuthClient');

    // Mock a delayed session resolution
    getSession.mockImplementation(() => {
      return new Promise((resolve) => {
        setTimeout(() => resolve(mockSessionWithUserId), 100);
      });
    });

    let authState;
    const TestObserver = () => {
      const auth = useAuth();
      authState = auth;
      return <div data-testid="observer">Observer</div>;
    };

    render(
      <AuthProvider>
        <TestObserver />
      </AuthProvider>
    );

    // Initially should be loading
    expect(authState.isLoading).toBe(true);

    // Wait for resolution
    await waitFor(() => {
      expect(authState.isLoading).toBe(false);
    }, { timeout: 5000 });

    // Should have user with ID
    expect(authState.user).toBeDefined();
    expect(authState.user.id).toBe('test-user-id-123');
  });
});

// Additional helper test to verify the auth context behavior
describe('Auth Context Behavior Verification', () => {
  test('Auth context provides user.id when available', async () => {
    const { getSession } = require('../config/betterAuthClient');
    getSession.mockResolvedValue(mockSessionWithUserId);

    let capturedAuthState;
    const CapturingComponent = () => {
      const auth = useAuth();
      capturedAuthState = auth;
      return <div>Test</div>;
    };

    render(
      <AuthProvider>
        <CapturingComponent />
      </AuthProvider>
    );

    // Wait for the async operation to complete
    await new Promise(resolve => setTimeout(resolve, 100));

    // Verify that the context eventually captures the correct state
    await waitFor(() => {
      expect(capturedAuthState.user?.id).toBe('test-user-id-123');
    }, { timeout: 3000 });
  });
});