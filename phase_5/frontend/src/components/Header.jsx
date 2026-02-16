import React from 'react';

const Header = ({ user, onMenuClick }) => {
  return (
    <header className="dashboard-header">
      <button
        className="menu-toggle"
        onClick={onMenuClick}
        aria-label="Toggle navigation menu"
      >
        ☰
      </button>

      <div className="header-content">
        <h1>Dashboard</h1>
      </div>

      <div className="header-actions">
        <div className="user-menu">
          <div className="user-avatar">
            {user?.name?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || '?'}
          </div>
          <span className="user-name">{user?.name || user?.email}</span>
        </div>
      </div>
    </header>
  );
};

export default Header;