import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Sidebar = ({ isOpen, onClose, user }) => {
  const { logout } = useAuth();
  const location = useLocation();

  const navItems = [
    { path: '/chat', label: 'Chat', icon: '💬' },
    { path: '/dashboard', label: 'Dashboard', icon: '🏠' },
    { path: '/tasks', label: 'Tasks', icon: '✅' },
    { path: '/analytics', label: 'Analytics', icon: '📊' },
  ];

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    logout();
    onClose();
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="sidebar-overlay"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`} role="navigation">
        <div className="sidebar-header">
          <h2>AI Assistant</h2>
        </div>

        <nav className="sidebar-nav">
          <ul>
            {navItems.map((item) => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`sidebar-link ${isActive(item.path) ? 'active' : ''}`}
                  onClick={onClose}
                >
                  <span className="sidebar-icon">{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              {user?.name?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || '?'}
            </div>
            <div className="user-details">
              <p className="user-name">{user?.name || user?.email}</p>
              <p className="user-email">{user?.email}</p>
            </div>
          </div>

          <button
            className="logout-btn"
            onClick={handleLogout}
            aria-label="Sign out"
          >
            <span>🚪</span>
            <span>Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;