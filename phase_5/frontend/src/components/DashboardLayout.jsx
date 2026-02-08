import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

const DashboardLayout = ({ children, user }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="dashboard-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} user={user} />
      <div className="dashboard-main">
        <Header
          user={user}
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        />
        <main className="dashboard-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;